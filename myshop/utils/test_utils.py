from django.urls import reverse


class Utils:
    """
    TODO
    """

    @staticmethod
    def reverse_with_next(view_name, next_view_name):
        """
        TODO
        """
        return f"{reverse(view_name)}?next={reverse(next_view_name)}"
