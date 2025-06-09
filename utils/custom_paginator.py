from typing import Any, List, Optional

from dlt.sources.helpers.rest_client.paginators import (BasePaginator,
                                                        PageNumberPaginator)
from requests import Request, Response


class CustomOffsetPaginator(BasePaginator):
    """A custom paginator for the Lucca API v3. It assumes a field that combine offset and limit separated by a comma.
    Stops when empty page is reached.

    Class is heavily inspired from the RangePaginator
    """

    def __init__(
        self,
        param_name: str,
        offset_initial_value: int,
        limit_value: int,
        base_index: int = 0,
        stop_after_empty_page: Optional[bool] = True,
    ):
        """
        Args:
            param_name (str): The query parameter name for the offset value.
                For example, 'page'.
            offset_initial_value (int): The initial value of the offset parameter.
            limit_value (int): The page limit (also defines the step size to increment the numeric parameter).
            base_index (int, optional): The index of the initial element.
                Used to define 0-based or 1-based indexing. Defaults to 0.
            stop_after_empty_page (bool): Whether pagination should stop when
              a page contains no result items. Defaults to `True`.
        """
        super().__init__()
        self.param_name = param_name
        self.initial_value = offset_initial_value
        self.current_value = offset_initial_value
        self.limit_value = limit_value
        self.base_index = base_index
        self.stop_after_empty_page = stop_after_empty_page

    def init_request(self, request: Request) -> None:
        self._has_next_page = True
        self.current_value = self.initial_value
        if request.params is None:
            request.params = {}

        request.params[self.param_name] = f"{self.current_value},{self.limit_value}"

    def update_state(
        self, response: Response, data: Optional[List[Any]] = None
    ) -> None:
        if self._stop_after_this_page(data):
            self._has_next_page = False
        else:
            self.current_value += self.limit_value

    def _stop_after_this_page(self, data: Optional[List[Any]] = None) -> bool:
        return self.stop_after_empty_page and not data # type: ignore

    def update_request(self, request: Request) -> None:
        if request.params is None:
            request.params = {}
        request.params[self.param_name] = f"{self.current_value},{self.limit_value}"


class PageNumberLimitPaginator(PageNumberPaginator):
    """A paginator using both page and limit parameter (used for the Lucca API v4).
    Stops when empty page is reached.
    """

    def __init__(
        self,
        limit: int,
        base_page: int = 0,
        page: int = None, # type: ignore
        page_param: str = "page",
        limit_param: str = "limit",
    ):
        super().__init__(
            base_page=base_page, page=page, page_param=page_param, total_path=None
        )
        self.limit = limit
        self.limit_param = limit_param

    def init_request(self, request: Request) -> None:
        super().init_request(request)
        request.params[self.limit_param] = self.limit

    def update_request(self, request: Request) -> None:
        super().update_request(request)
        request.params[self.limit_param] = self.limit
