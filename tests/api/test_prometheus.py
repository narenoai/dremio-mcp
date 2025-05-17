import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from dremioai.api.prometheus import vm
from dremioai.config import settings
from dremioai.config.settings import Prometheus


@pytest.mark.asyncio
async def test_get_promql_result_converts_start_datetime(mock_settings_instance):
    settings.instance().prometheus = Prometheus(uri="http://example.com", token="t")

    dummy = vm.PromQLResult(status=vm.PromQLResultStatus.SUCCESS, data=vm.TimeSeriesData())
    async_mock = AsyncMock(return_value=dummy)
    with patch.object(vm.AsyncHttpClient, "get", async_mock) as mock_get:
        dt = datetime(2024, 1, 1, 0, 0, 0)
        await vm.get_promql_result("up", start=dt)
        params = mock_get.call_args.kwargs["params"]
        assert pytest.approx(params["start"], rel=1e-3) == dt.timestamp()

@pytest.mark.asyncio
async def test_get_promql_result_converts_end_datetime(mock_settings_instance):
    settings.instance().prometheus = Prometheus(uri="http://example.com", token="t")

    dummy = vm.PromQLResult(status=vm.PromQLResultStatus.SUCCESS, data=vm.TimeSeriesData())
    async_mock = AsyncMock(return_value=dummy)
    with patch.object(vm.AsyncHttpClient, "get", async_mock) as mock_get:
        dt = datetime(2024, 1, 1, 1, 0, 0)
        await vm.get_promql_result("up", end=dt)
        params = mock_get.call_args.kwargs["params"]
        assert pytest.approx(params["end"], rel=1e-3) == dt.timestamp()

