
try:

    from zcrmsdk.src.com.zoho.crm.api.dc.data_center import DataCenter

except Exception as e:

    from .data_center import DataCenter


class USDataCenter(DataCenter):

    """
    This class representing the US countries Zoho CRM and Accounts URL. It is used to denote the domain of the user.
    """

    @classmethod
    def PRODUCTION(cls):

        """
        This Environment class instance represents the US countries Zoho CRM production environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://www.zohoapis.com", cls().get_iam_url(), cls().get_file_upload_url())

    @classmethod
    def SANDBOX(cls):

        """
        This Environment class instance represents the US countries Zoho CRM sandbox environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://sandbox.zohoapis.com", cls().get_iam_url(), cls().get_file_upload_url())

    @classmethod
    def DEVELOPER(cls):

        """
        This Environment class instance represents the US countries Zoho CRM developer environment.
        :return: A Environment class instance.
        """

        return DataCenter.Environment("https://developer.zohoapis.com", cls().get_iam_url(), cls().get_file_upload_url())

    def get_iam_url(self):

        """
        This method to get accounts URL.
        :return: A str representing the accounts URL.
        """

        return "https://accounts.zoho.com/oauth/v2/token"

    def get_file_upload_url(self):
        """
        The method to get File Upload URL
        :return: A str representing the File Upload URL
        """

        return "https://content.zohoapis.com"
