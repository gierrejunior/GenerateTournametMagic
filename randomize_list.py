import random


class RandomizeList:
    """_summary_
    """
    def randomizeList(self, times: int, _list: list) -> list:
        """_summary_

        Args:
            times (_type_): _description_
            _list (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if not _list:
            raise ValueError(
                "RandomizeList: The list is empty."
                " You cannot randomize an empty list.")
        result_list = []
        for i in range(times):
            result = random.choice(_list)
            _list.remove(result)
            result_list.append(result)
        return result_list

    def randomizelists(self, *args: list) -> list:
        """_summary_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        result_list = []
        deck_choiced = ""
        for _list in args:
            if not _list:
                raise ValueError(
                    "RandomizeList: The list is empty."
                    " You cannot randomize an empty list.")
            if deck_choiced:
                if deck_choiced in _list:
                    _list.remove(deck_choiced)
            result = random.choice(_list)
            deck_choiced = result
            result_list.append(result)
        return result_list
