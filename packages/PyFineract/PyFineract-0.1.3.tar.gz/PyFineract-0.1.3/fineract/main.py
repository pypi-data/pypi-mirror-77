# fineract APIs run on https by default
from fineract import ResourceNotFoundException
from fineract.handlers import RequestHandler
from fineract.objects import Savings
from fineract.objects.client import Client
from fineract.objects.group import Group
from fineract.objects.hook import Hook
from fineract.objects.loan import Loan
from fineract.objects.loan_product import LoanProduct
from fineract.objects.org import Staff, Fund, Charge, Office
from fineract.objects.report import Report
from fineract.objects.role import Role
from fineract.objects.user import User
from fineract.pagination import PaginatedList
from fineract.templates import TEMPLATES

DEFAULT_BASE_URL = 'https://localhost/fineract-provider/api/v1'
DEFAULT_TENANT = 'default'
DEFAULT_TIMEOUT = 15
DEFAULT_PER_PAGE = 30


class Fineract(object):
    """Provide a Fineract object


    :param per_page: int Number of items per page
    :param debug: bool Enable debug mode
    :param ssl_check: bool Verify ssl certs
    :param username: str Fineract Username
    :param password: str Fineract Password
    :param tenant:  str Fineract Tenant
    :param base_url: string Fineract base url
    :param timeout: int Request timeout
    """

    def __init__(self, username=None, password=None, tenant=DEFAULT_TENANT, base_url=DEFAULT_BASE_URL,
                 timeout=DEFAULT_TIMEOUT, per_page=DEFAULT_PER_PAGE, debug=False, ssl_check=True):

        assert username is None or isinstance(username, str), username
        assert password is None or isinstance(password, str), password
        assert tenant is None or isinstance(tenant, str), tenant
        assert base_url is None or isinstance(base_url, str), base_url
        self.__request_handler = RequestHandler(username, password, base_url, tenant, timeout, per_page, debug,
                                                ssl_check)

    @property
    def request_handler(self):
        """:class:`fineract.handlers.RequestHandler`"""
        return self.__request_handler

    def get_roles(self):
        """Returns all roles

        :calls `GET /roles <https://demo.openmf.org/api-docs/apiLive.htm#roles>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.role.Role`
        """
        return PaginatedList(
            Role,
            self.__request_handler,
            '/roles',
            dict()
        )

    def get_clients(self, **kwargs):
        """Returns all clients

        :calls `GET /clients <https://demo.openmf.org/api-docs/apiLive.htm#clients>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.client.Client`
        """
        return PaginatedList(
            Client,
            self.__request_handler,
            '/clients',
            kwargs
        )

    def get_client(self, id, **kwargs):
        """Returns a client with id

        :calls `GET /clients/<id> <https://demo.openmf.org/api-docs/apiLive.htm#clients_retrieve>`_

        :param id: int Client id
        :rtype: :class:`fineract.objects.client.Client`
        """
        return Client(self.__request_handler,
                      self.__request_handler.make_request(
                          'GET',
                          '/clients/{}'.format(id),
                          params=kwargs
                      ), False)

    def get_loan_products(self, **kwargs):
        """Returns all loan products

        :calls `GET /loanproducts <https://demo.openmf.org/api-docs/apiLive.htm#loanproducts>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.loan_product.LoanProduct`
        """
        return PaginatedList(
            LoanProduct,
            self.__request_handler,
            '/loanproducts',
            kwargs
        )

    def get_loan_product(self, id, **kwargs):
        """Return a loan product with matching id

        :calls `GET /loanproducts/<id> <https://demo.openmf.org/api-docs/apiLive.htm#loanproducts_retrieve>`_

        :param id: int Loan Product id
        :rtype: :class:`fineract.objects.loan_product.LoanProduct`
        """
        return LoanProduct(self.__request_handler,
                           self.__request_handler.make_request(
                               'GET',
                               '/loanproducts/{}'.format(id),
                               params=kwargs
                           ), False)

    def get_loans(self, **kwargs):
        """Return all loans

        :calls `GET /loans <https://demo.openmf.org/api-docs/apiLive.htm#loans>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.loan.Loan`
        """
        return PaginatedList(
            Loan,
            self.__request_handler,
            '/loans',
            kwargs
        )

    def get_loan(self, id, **kwargs):
        """Returns a loan with matching id

        :calls `GET /loans/<id> <https://demo.openmf.org/api-docs/apiLive.htm#loans_retrieve>`_

        :param id: int Loan id
        :rtype: :class:`fineract.objects.loan.Loan`
        """
        return Loan(self.__request_handler,
                    self.__request_handler.make_request(
                        'GET',
                        '/loans/{}'.format(id),
                        params=kwargs
                    ), False)

    def get_savings_accounts(self, **kwargs):
        """Return all savings accounts

        :calls `GET /loans <https://demo.openmf.org/api-docs/apiLive.htm#savingsaccounts>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.savings.Savings`
        """
        return PaginatedList(
            Savings,
            self.__request_handler,
            '/savingsaccounts',
            kwargs
        )

    def get_savings_account(self, id, **kwargs):
        """Returns a savings account with matching id

        :calls `GET /savingsaccounts/<id> <https://demo.openmf.org/api-docs/apiLive.htm#savingsaccounts_retrieve>`_

        :param id: int Savings account id
        :rtype: :class:`fineract.objects.savings.Savings`
        """
        return Savings(self.__request_handler,
                       self.__request_handler.make_request(
                           'GET',
                           '/savingsaccounts/{}'.format(id),
                           params=kwargs
                       ), False)

    def get_staff(self, id=None):
        """Returns a stuff with a matching id or all staff

        :calls `GET /staff/<id> <https://demo.openmf.org/api-docs/apiLive.htm#staff_retrieve>`_

        :param id: Staff id
        :rtype: :class:`fineract.objects.staff.Staff` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.org.Staff`
        """
        if id:
            return Staff(self.__request_handler,
                         self.__request_handler.make_request(
                             'GET',
                             '/staff/{}'.format(id),
                         ), False)
        else:
            return PaginatedList(
                Staff,
                self.__request_handler,
                '/staff',
                dict()
            )

    def get_funds(self, id=None):
        """"Returns a fund with a matching id or all funds

        :calls `GET /funds/<id> <https://demo.openmf.org/api-docs/apiLive.htm#funds_retrieve>`_

        :param id: Charge id
        :rtype: :class:`fineract.objects.org.Fund` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.org.Fund`
        """
        if id:
            return Fund(self.__request_handler,
                        self.__request_handler.make_request(
                            'GET',
                            '/funds/{}'.format(id),
                        ), False)
        else:
            return PaginatedList(
                Fund,
                self.__request_handler,
                '/funds',
                dict()
            )

    def get_charges(self, id=None):
        """Returns a charge with a matching id or all charges

        :calls `GET /charges/<id> <https://demo.openmf.org/api-docs/apiLive.htm#charges_retrieve>`_

        :param id: Charge id
        :rtype: :class:`fineract.objects.org.Charge` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.org.Charge`
        """
        if id:
            return Charge(self.__request_handler,
                          self.__request_handler.make_request(
                              'GET',
                              '/charges/{}'.format(id),
                          ), False)
        else:
            return PaginatedList(
                Charge,
                self.__request_handler,
                '/charges',
                dict()
            )

    def get_offices(self, id=None):
        """Returns an office with a matching id or all offices

        :calls `GET /offices/<id> <https://demo.openmf.org/api-docs/apiLive.htm#offices_retrieve>`_

        :param id: Office id
        :rtype: :class:`fineract.objects.org.Office` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.org.Office`
        """
        if id:
            return Office(self.__request_handler,
                          self.__request_handler.make_request(
                              'GET',
                              '/offices/{}'.format(id),
                          ), False)
        else:
            return PaginatedList(
                Office,
                self.__request_handler,
                '/offices',
                dict()
            )

    def get_groups(self, **kwargs):
        """Returns all groups

        :calls `GET /groups <https://demo.openmf.org/api-docs/apiLive.htm#groups>`_

        :rtype: :class:`fineract.pagination.PaginatedList` of :class:`fineract.objects.group.Group`
        """
        return PaginatedList(
            Group,
            self.__request_handler,
            '/groups',
            kwargs
        )

    def get_group(self, id, **kwargs):
        """Returns a group with id

        :calls `GET /groups/<id> <https://demo.openmf.org/api-docs/apiLive.htm#groups_retrieve>`_

        :param id: int Group id
        :rtype: :class:`fineract.objects.group.Group`
        """
        return Group(self.__request_handler,
                     self.__request_handler.make_request(
                         'GET',
                         '/groups/{}'.format(id),
                         params=kwargs
                     ), False)

    def get_reports(self, id=None):
        """Returns an office with a matching id or all offices

        :calls `GET /reports/<id> <https://demo.openmf.org/api-docs/apiLive.htm#reports_retrieve>`_

        :param id: Office id
        :rtype: :class:`fineract.objects.report.Report` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.report.Report`
        """
        if id:
            return Report(self.__request_handler,
                          self.__request_handler.make_request(
                              'GET',
                              '/reports/{}'.format(id),
                          ), False)
        else:
            return PaginatedList(
                Report,
                self.__request_handler,
                '/reports',
                dict()
            )

    def get_hooks(self, id=None):
        """Returns an office with a matching id or all offices

        :calls `GET /hooks/<id> <https://demo.openmf.org/api-docs/apiLive.htm#hooks_retrieve>`_

        :param id: Office id
        :rtype: :class:`fineract.objects.hook.Hook` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.hook.Hook`
        """
        if id:
            return Hook(self.__request_handler,
                        self.__request_handler.make_request(
                            'GET',
                            '/hooks/{}'.format(id),
                        ), False)
        else:
            return PaginatedList(
                Hook,
                self.__request_handler,
                '/hooks',
                dict()
            )

    def get_users(self, id=None):
        """Returns an user with a matching id or all users

        :calls `GET /users/<id> <https://demo.openmf.org/api-docs/apiLive.htm#users_retrieve>`_

        :param id: User id
        :rtype: :class:`fineract.objects.user.User` or  :class:`fineract.pagination.PaginatedList` of
            :class:`fineract.objects.user.User`
        """
        if id:
            return User(self.__request_handler,
                        self.__request_handler.make_request(
                            'GET',
                            '/users/{}'.format(id),
                        ), False)
        else:
            return PaginatedList(
                User,
                self.__request_handler,
                '/users',
                dict()
            )

    def raw_request(self, method, url, **kwargs):
        """Make a raw request to the Fineract API

        :param method: request method
        :param url: endpoint
        :param kwargs:
        :return: Returns dict/list object
        """
        return self.__request_handler.make_request(method, url, **kwargs)

    def templates(self, template, extra=None, params=None):
        """Retrieve a template
        :param template: template name
        :param extra:
        :return:
        """
        template_url = TEMPLATES.get(template, '')
        if not template_url:
            raise ResourceNotFoundException(404, 'Template not found')
        if extra:
            template_url = template_url.format(extra)

        if params:
            template_url += '&' + params

        return self.__request_handler.make_request('GET', '/' + template_url)
