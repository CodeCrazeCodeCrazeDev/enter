from __future__ import annotations
import json

class TrajectoryDatasetCompiler:
    def __init__(self, max_self_generated_ratio: float = 0.5, strict_mode: bool = False, output_format: str = "openai") -> None:
        self.max_self_generated_ratio = max_self_generated_ratio
        self.strict_mode = strict_mode
        self.output_format = output_format

    def compile_trajectory(self, history: list[dict], is_success: bool) -> list[dict]:
        if not is_success:
            return []

        compiled = []
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "tool":
                role = "user"
                content = f"[Tool Output] {content}"
            compiled.append({"role": role, "content": content})
        return compiled

    def export_to_jsonl(self, input_data: list, jsonl_file: str) -> None:
        if input_data and isinstance(input_data[0], dict) and "messages" in input_data[0]:
            self_gen_count = sum(1 for item in input_data if item.get("is_self_generated", False))
            total = len(input_data)
            ratio = self_gen_count / total if total else 0.0

            if ratio > self.max_self_generated_ratio:
                if self.strict_mode:
                    raise ValueError("Model-Collapse Guard: Self-generated data ratio exceeds maximum threshold.")

                real_data = [item for item in input_data if not item.get("is_self_generated", False)]
                self_gen_data = [item for item in input_data if item.get("is_self_generated", False)]
                self_gen_data.sort(key=lambda x: x.get("score", 0.0), reverse=True)
                max_self_gen = max(1, int((self.max_self_generated_ratio * len(real_data)) / max(1e-5, (1.0 - self.max_self_generated_ratio))))
                kept = real_data + self_gen_data[:max_self_gen]
            else:
                kept = input_data

            with open(jsonl_file, "w", encoding="utf-8") as f:
                for item in kept:
                    f.write(json.dumps(item) + "\n")
        else:
            with open(jsonl_file, "w", encoding="utf-8") as f:
                for messages in input_data:
                    f.write(json.dumps({"messages": messages}) + "\n")

class TwoLevelCreditAssignment:
    def assign_credit(self, trajectory: dict, is_success: bool) -> dict:
        traj_credit = 1.0 if is_success else -0.5
        steps = trajectory.get("steps", [])
        step_credits = []
        n = len(steps)
        for i, step in enumerate(steps):
            scale = (i + 1) / n if n else 1.0
            step_credits.append({
                "step": step.get("step"),
                "credit": traj_credit * scale if is_success else -0.2 * scale
            })
        return {
            "trajectory_credit": traj_credit,
            "step_credits": step_credits
        }

class MultiDimensionalTrajectoryVerifier:
    def verify_trajectory(self, messages: list[dict]) -> dict:
        syntax_score = 1.0
        assistant_contents = [msg.get("content", "") for msg in messages if msg.get("role") == "assistant"]
        has_duplicates = len(assistant_contents) != len(set(assistant_contents))

        for msg in messages:
            content = msg.get("content", "")
            opened = []
            mapping = {")": "(", "}": "{", "]": "["}
            for char in content:
                if char in mapping.values():
                    opened.append(char)
                elif char in mapping.keys():
                    if not opened or opened[-1] != mapping[char]:
                        syntax_score = 0.5
                        break
                    opened.pop()
            if len(opened) > 0:
                syntax_score = 0.5

        efficiency_score = 0.5 if has_duplicates else 1.0
        is_high_quality = syntax_score == 1.0 and efficiency_score == 1.0

        return {
            "is_high_quality": is_high_quality,
            "syntax_score": syntax_score,
            "efficiency_score": efficiency_score
        }
