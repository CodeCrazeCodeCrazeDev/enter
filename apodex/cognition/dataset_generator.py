from __future__ import annotations
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("apodex.cognition")


class TrajectoryDatasetCompiler:
    """Compiles trajectories into standardized fine-tuning datasets with strict E9 Model-Collapse guards."""

    def __init__(self, output_format: str = "openai", max_self_generated_ratio: float = 0.5, strict_mode: bool = False) -> None:
        self.output_format = output_format
        self.max_self_generated_ratio = max_self_generated_ratio
        self.strict_mode = strict_mode

    def compile_trajectory(self, raw_history: List[Dict[str, Any]], is_success: bool) -> List[Dict[str, Any]]:
        """Format and clean a raw trajectory history. Skips unsuccessful runs."""
        if not is_success:
            return []

        formatted = []
        for message in raw_history:
            role = message.get("role")
            content = message.get("content", "")

            # Convert tool messages to user prompts with prefix [Tool Output]
            if role == "tool":
                formatted.append({
                    "role": "user",
                    "content": f"[Tool Output] {content}"
                })
            else:
                formatted.append({
                    "role": role,
                    "content": content
                })
        return formatted

    def export_to_jsonl(self, trajectories: List[List[Dict[str, Any]]], output_path: str) -> None:
        """Export trajectories to JSONL format. Includes E9 Model-Collapse check and downsampling."""
        # Note: input_data might be passed as dictionaries with "messages" and "is_self_generated"
        # We need to support both a list of formatted lists, and a list of dictionaries.
        records = []
        self_generated_count = 0

        for item in trajectories:
            if isinstance(item, dict):
                msg_list = item.get("messages", [])
                is_self = item.get("is_self_generated", False)
                score = item.get("score", 1.0)
                records.append({
                    "messages": msg_list,
                    "is_self_generated": is_self,
                    "score": score
                })
                if is_self:
                    self_generated_count += 1
            else:
                # Fallback assuming list of messages
                records.append({
                    "messages": item,
                    "is_self_generated": False,
                    "score": 1.0
                })

        total = len(records)
        ratio = (self_generated_count / total) if total > 0 else 0.0

        if ratio > self.max_self_generated_ratio:
            msg = f"Model-Collapse Guard: Self-generated data ratio is {ratio:.2%}, which exceeds the limit of {self.max_self_generated_ratio:.2%}."
            if self.strict_mode:
                logger.error(msg)
                raise ValueError(msg)
            else:
                logger.warning(f"{msg} Automatically downsampling self-generated data.")
                # Non-strict: Downsample self-generated records keeping the highest scores
                reals = [r for r in records if not r["is_self_generated"]]
                selfs = [r for r in records if r["is_self_generated"]]

                # Calculate allowed number of self-generated items
                # We want: selfs_kept / (reals + selfs_kept) <= max_self_generated_ratio
                # selfs_kept <= (reals * max_ratio) / (1 - max_ratio)
                allowed_selfs = int((len(reals) * self.max_self_generated_ratio) / (1 - self.max_self_generated_ratio)) if self.max_self_generated_ratio < 1.0 else len(selfs)
                allowed_selfs = max(allowed_selfs, 0)

                # Sort selfs by score descending, keep top allowed_selfs
                selfs.sort(key=lambda x: x["score"], reverse=True)
                selfs_kept = selfs[:allowed_selfs]

                records = reals + selfs_kept

        # Write to JSONL
        with open(output_path, "w", encoding="utf-8") as f:
            for rec in records:
                # standard openai jsonl format has a messages block
                f.write(json.dumps({"messages": rec["messages"]}) + "\n")
