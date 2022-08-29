from django.urls import reverse


class Utils:
    """
    TODO
    """

    @staticmethod
    def reverse_with_next(view_name, next_view_name, **kwargs):
        """
        TODO
        """
        return (
            f"{reverse(view_name, kwargs=kwargs.get('base_kwargs'))}"
            f"?next={reverse(next_view_name, kwargs=kwargs.get('next_kwargs'))}"
        )
