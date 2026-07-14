from __future__ import annotations

import pytest

from apodex.arcs.service_registry import ServiceRegistry


class IExampleService:
    pass


class ExampleServiceImpl(IExampleService):
    pass


@pytest.fixture(autouse=True)
def _reset_registry():
    ServiceRegistry().reset()
    yield
    ServiceRegistry().reset()


def test_registry_is_singleton():
    assert ServiceRegistry() is ServiceRegistry()


def test_register_and_resolve():
    registry = ServiceRegistry()
    impl = ExampleServiceImpl()
    registry.register(IExampleService, impl)
    assert registry.resolve(IExampleService) is impl


def test_resolve_unregistered_raises():
    with pytest.raises(ValueError, match="is not registered"):
        ServiceRegistry().resolve(IExampleService)


def test_has_service():
    registry = ServiceRegistry()
    assert registry.has_service(IExampleService) is False
    registry.register(IExampleService, ExampleServiceImpl())
    assert registry.has_service(IExampleService) is True


def test_reset_clears_services():
    registry = ServiceRegistry()
    registry.register(IExampleService, ExampleServiceImpl())
    registry.reset()
    assert registry.has_service(IExampleService) is False
