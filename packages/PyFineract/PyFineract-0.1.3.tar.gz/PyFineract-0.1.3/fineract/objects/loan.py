from datetime import datetime

from fineract.objects.currency import Currency
from fineract.objects.fineract_object import DataFineractObject, FineractObject
from fineract.objects.types import LoanType, TermPeriodFrequencyType, Type


class Loan(DataFineractObject):
    """
    This class represents a Loan.
    """

    def __repr__(self):
        return self.get__repr__({'loan_id': self.id})

    def _init_attributes(self):
        self.id = None
        self.account_no = None
        self.status = None
        self.external_id = None
        self.client_id = None
        self.loan_product_id = None
        self.loan_purpose_id = None
        self.loan_purpose_name = None
        self.loan_type = None
        self.currency = None
        self.principal = None
        self.term_frequency = None
        self.term_frequency_type = None
        self.timeline = None
        self.transactions = None
        self.summary = None
        self.multi_disburse_loan = None
        self.can_define_installment_amount = None
        self.can_disburse = None
        self.can_use_for_topup = None
        self.is_topup = None
        self.in_arrears = None
        self.is_npa = None

    def _use_attributes(self, attributes):
        self.id = attributes.get('id', None)
        self.account_no = attributes.get('accountNo', None)
        self.status = self._make_fineract_object(LoanStatus, attributes.get('status', None))
        self.external_id = attributes.get('externalId', None)
        self.client_id = attributes.get('clientId', None)
        self.loan_product_id = attributes.get('loanProductId', None)
        self.loan_purpose_id = attributes.get('loanPurposeId', None)
        self.loan_purpose_name = attributes.get('loanPurposeName', None)
        self.loan_type = self._make_fineract_object(LoanType, attributes.get('loanType', None))
        self.currency = self._make_fineract_object(Currency, attributes.get('currency', None))
        self.principal = attributes.get('principal', None)
        self.term_frequency = attributes.get('termFrequency', None)
        self.term_frequency_type = self._make_fineract_object(TermPeriodFrequencyType,
                                                              attributes.get('termPeriodFrequencyType', None))
        self.timeline = self._make_fineract_object(LoanTimeline, attributes.get('timeline', None))
        self.transactions = self._make_fineract_objects_list(LoanTransaction, attributes.get('transactions', None))
        self.summary = self._make_fineract_object(LoanSummary, attributes.get('summary', None))
        self.multi_disburse_loan = attributes.get('multiDisburseLoan', None)
        self.can_define_installment_amount = attributes.get('canDefineInstallmentAmount', None)
        self.can_disburse = attributes.get('canDisburse', None)
        self.can_use_for_topup = attributes.get('canUseForTopup', None)
        self.is_topup = attributes.get('isTopup', None)
        self.in_arrears = attributes.get('inArrears', None)
        self.is_npa = attributes.get('isNPA', None)

    def days_in_arrears(self) -> int:
        """Return the number of days in arrears

        :return: int
        """
        in_arrears = -1
        if self.in_arrears:
            delta = datetime.today() - self.timeline.expected_maturity_date
            in_arrears = delta.days

        return in_arrears

    def is_closed(self) -> bool:
        """Check whether a loan is closed or not

        :return: bool
        """
        return self.status is not None and self.status.closed

    @staticmethod
    def template(request_handler, client_id=None, template_type='individual', product_id=None) -> bool:
        """Get a loan template

        :param template_type:
        :param product_id:
        :param client_id:
        :param request_handler:
        :return: dict
        """
        if client_id and product_id:
            return request_handler.make_request(
                'GET',
                '/loans/template?templateType={}&clientId={}&productId={}'.format(template_type, client_id, product_id)
            )

        return request_handler.make_request(
            'GET',
            '/loans/template?templateType={}&clientId={}'.format(template_type, client_id)
        )

    @classmethod
    def apply(cls, request_handler, client_id, product_id, principal, expected_disbursement_date=datetime.now(),
              submitted_date=datetime.now(), **kwargs) \
            -> 'Loan':
        """Submit a new loan application

        :param submitted_date:
        :param request_handler:
        :param client_id:
        :param product_id:
        :param principal:
        :param expected_disbursement_date:
        :return: :class:`fineract.objects.loan.Loan`
        """
        template = cls.template(request_handler, client_id, product_id=product_id)
        payload = {
            'clientId': client_id,
            'productId': product_id,
            'principal': principal,
            'loanTermFrequency': template['termFrequency'],
            'loanTermFrequencyType': template['termPeriodFrequencyType']['id'],
            'loanType': 'individual',
            'numberOfRepayments': template['numberOfRepayments'],
            'repaymentEvery': template['repaymentEvery'],
            'repaymentFrequencyType': template['repaymentFrequencyType']['id'],
            'interestRatePerPeriod': template['interestRatePerPeriod'],
            'amortizationType': template['amortizationType']['id'],
            'interestType': template['interestType']['id'],
            'interestCalculationPeriodType': template['interestCalculationPeriodType']['id'],
            'transactionProcessingStrategyId': template['transactionProcessingStrategyId'],
            'expectedDisbursementDate': expected_disbursement_date,
            'submittedOnDate': submitted_date,
        }
        payload.update(kwargs)

        res = request_handler.make_request(
            'POST',
            '/loans',
            json=payload
        )

        loan_id = res['loanId']
        return cls(request_handler,
                   request_handler.make_request(
                       'GET',
                       '/loans/{}'.format(loan_id)
                   ), False)

    def delete(self) -> bool:
        """Delete a loan application. Only loans with status of "Submitted and awaiting approval"

        :return: bool
        """
        res = self.request_handler.make_request(
            'DELETE',
            '/loans/{}'.format(self.id)
        )
        return res['loanId'] == self.id

    def reject(self, note, rejected_on_date=datetime.now()):
        res = self.request_handler.make_request(
            'POST',
            '/loans/{}?command=reject'.format(self.id),
            json={'note': note, 'rejectedOnDate': rejected_on_date}
        )
        return res['loanId'] == self.id

    def approve(self, approved_on_date=datetime.now(), approved_loan_amount=None, expected_disbursement_date=None) \
            -> bool:
        """Approve a loan application

        :param approved_on_date:
        :param approved_loan_amount:
        :param expected_disbursement_date:
        :return: bool
        """
        payload = {
            'approvedOnDate': approved_on_date
        }

        if approved_loan_amount:
            payload['approvedLoanAmount'] = approved_loan_amount

        if expected_disbursement_date:
            payload['expectedDisbursementDate'] = expected_disbursement_date

        res = self.request_handler.make_request(
            'POST',
            '/loans/{}?command=approve'.format(self.id),
            json=payload
        )
        return res['loanId'] == self.id

    def undo_approval(self, note) -> bool:
        res = self.request_handler.make_request(
            'POST',
            '/loans/{}?command=undoApproval'.format(self.id),
            json={'note': note}
        )
        return res['loanId'] == self.id

    def disburse(self, actual_disbursement_date=datetime.now(), transaction_amount=None, fixed_emi_amount=None) -> bool:
        """Disburse an approved loan application

        :param actual_disbursement_date:
        :param transaction_amount:
        :param fixed_emi_amount:
        :return: bool
        """
        payload = {
            'actualDisbursementDate': actual_disbursement_date
        }

        if transaction_amount:
            payload['transactionAmount'] = transaction_amount

        if fixed_emi_amount:
            payload['fixedEmiAmount'] = fixed_emi_amount

        res = self.request_handler.make_request(
            'POST',
            '/loans/{}?command=disburse'.format(self.id),
            json=payload
        )
        return res['loanId'] == self.id

    # def disburse_to_savings(self, actual_disbursement_date=datetime.now(), transaction_amount=None, fixed_emi_amount=None):
    #     """Disburse an approved loan application to savings
    #
    #     :param actual_disbursement_date:
    #     :param transaction_amount:
    #     :param fixed_emi_amount:
    #     :return: bool
    #     """
    #     payload = {
    #         'actualDisbursementDate': actual_disbursement_date
    #     }
    #
    #     if transaction_amount:
    #         payload['transactionAmount'] = transaction_amount
    #
    #     if fixed_emi_amount:
    #         payload['fixedEmiAmount'] = fixed_emi_amount
    #
    #     res = self.request_handler.make_request(
    #         'POST',
    #         '/loans/{}?command=disburseToSavings'.format(self.id),
    #         json=payload
    #     )
    #     return res['loanId'] == self.id

    def undo_disbursal(self, note) -> bool:
        res = self.request_handler.make_request(
            'POST',
            '/loans/{}?command=undoDisbursal'.format(self.id),
            json={'note': note}
        )
        return res['loanId'] == self.id

    def make_repayment(self, amount, transaction_date, **kwargs):
        """Make a repayment on a loan

        :param amount:
        :param transaction_date:
        :param kwargs: Extra args see https://demo.mifos.io/api-docs/apiLive.htm#loans_transactions
        :return: bool
        """
        payload = {
            'transactionDate': transaction_date,
            'transactionAmount': amount
        }
        payload.update(kwargs)
        # print(payload)
        res = self.request_handler.make_request(
            'POST',
            '/loans/{}/transactions?command=repayment'.format(self.id),
            json=payload
        )
        return res['loanId'] == self.id

    def apply_charge(self, charge_id, amount, due_date=datetime.now()):
        res = self.request_handler.make_request(
            'POST',
            '/loans/{}/charges'.format(self.id),
            json={'chargeId': charge_id, 'amount': amount, 'dueDate': due_date}
        )
        return res['loanId'] == self.id


class LoanStatus(FineractObject):

    def _init_attributes(self):
        self.id = None
        self.code = None
        self.value = None
        self.pending_approval = None
        self.waiting_for_disbursal = None
        self.active = None
        self.closed_obligations_met = None
        self.close_written_off = None
        self.written_off = None
        self.closed_rescheduled = None
        self.closed = None
        self.overpaid = None

    def _use_attributes(self, attributes):
        self.id = attributes.get('id', None)
        self.code = attributes.get('code', None)
        self.value = attributes.get('value', None)
        self.pending_approval = attributes.get('pendingApproval', None)
        self.waiting_for_disbursal = attributes.get('waitingForDisbursal', None)
        self.active = attributes.get('active', None)
        self.closed_obligations_met = attributes.get('closedObligationsMet', None)
        self.close_written_off = attributes.get('closedWrittenOff', None)
        self.closed_rescheduled = attributes.get('closedRescheduled', None)
        self.closed = attributes.get('closed', None)
        self.overpaid = attributes.get('overpaid', None)


class LoanTimeline(FineractObject):
    """
    This class represent the timeline of a Loan
    """

    def _init_attributes(self):
        self.submitted_on = None
        self.submitted_by = None
        self.approved_on = None
        self.approved_by = None
        self.expected_disbursement_date = None
        self.actual_disbursement_date = None
        self.disbursed_by = None
        self.closed_on_date = None
        self.expected_maturity_date = None

    def _use_attributes(self, attributes):
        self.submitted_on = self._make_date_object(attributes.get('submittedOnDate', None))
        self.submitted_by = attributes.get('submittedByUsername', None)
        self.approved_on = self._make_date_object(attributes.get('approvedOnDate', None))
        self.approved_by = attributes.get('approvedByUsername', None)
        self.expected_disbursement_date = self._make_date_object(attributes.get('expectedDisbursementDate', None))
        self.actual_disbursement_date = self._make_date_object(attributes.get('actualDisbursementDate', None))
        self.disbursed_by = attributes.get('disbursedByUsername', None)
        self.closed_on_date = self._make_date_object(attributes.get('closedOnDate', None))
        self.expected_maturity_date = self._make_date_object(attributes.get('expectedMaturityDate', None))


class LoanSummary(FineractObject):
    """
    This is the summary of a Loan
    """

    def _init_attributes(self):
        self.principal_disbursed = None
        self.principal_paid = None
        self.principal_written_off = None
        self.principal_outstanding = None
        self.principal_overdue = None
        self.interest_charged = None
        self.interest_paid = None
        self.interest_waived = None
        self.interest_written_off = None
        self.interest_outstanding = None
        self.interest_overdue = None
        self.fee_charges_charged = None
        self.fee_charges_due_at_disbursement = None
        self.fee_charges_paid = None
        self.fee_charges_waived = None
        self.fee_charges_written_off = None
        self.fee_charges_outstanding = None
        self.fee_charges_overdue = None
        self.penalty_charges_charged = None
        self.penalty_charges_paid = None
        self.penalty_charges_waived = None
        self.penalty_charges_written_off = None
        self.penalty_charges_outstanding = None
        self.penalty_charges_overdue = None
        self.total_expected_repayment = None
        self.total_repayment = None
        self.total_expected_cost_of_loan = None
        self.total_cost_of_loan = None
        self.total_waived = None
        self.total_written_off = None
        self.total_overdue = None
        self.total_outstanding = None
        self.overdue_since_date = None
        self.in_arrears = None
        self.is_npa = None

    def _use_attributes(self, attributes):
        self.principal_disbursed = attributes.get('principalDisbursed', None)
        self.principal_paid = attributes.get('principalPaid', None)
        self.principal_written_off = attributes.get('principalWrittenOff', None)
        self.principal_outstanding = attributes.get('principalOutstanding', None)
        self.principal_overdue = attributes.get('principalOverdue', None)
        self.interest_charged = attributes.get('interestCharged', None)
        self.interest_paid = attributes.get('interestPaid', None)
        self.interest_waived = attributes.get('interestWaived', None)
        self.interest_written_off = attributes.get('interestWrittenOff', None)
        self.interest_outstanding = attributes.get('interestOutstanding', None)
        self.interest_overdue = attributes.get('interestOverdue', None)
        self.fee_charges_charged = attributes.get('feeChargesCharged', None)
        self.fee_charges_due_at_disbursement = attributes.get('feeChargesDueAtDisbursementCharged', None)
        self.fee_charges_paid = attributes.get('feeChargesPaid', None)
        self.fee_charges_waived = attributes.get('feeChargesWaived', None)
        self.fee_charges_written_off = attributes.get('feeChargesWrittenOff', None)
        self.fee_charges_outstanding = attributes.get('feeChargesOutstanding', None)
        self.fee_charges_overdue = attributes.get('feeChargesOverdue', None)
        self.penalty_charges_charged = attributes.get('penaltyChargesCharged', None)
        self.penalty_charges_paid = attributes.get('penaltyChargesPaid', None)
        self.penalty_charges_waived = attributes.get('penaltyChargesWaived', None)
        self.penalty_charges_written_off = attributes.get('penaltyChargesWrittenOff', None)
        self.penalty_charges_outstanding = attributes.get('penaltyChargesOutstanding', None)
        self.penalty_charges_overdue = attributes.get('penaltyChargesOverdue', None)
        self.total_expected_repayment = attributes.get('totalExpectedRepayment', None)
        self.total_repayment = attributes.get('totalRepayment', None)
        self.total_expected_cost_of_loan = attributes.get('totalExpectedCostOfLoan', None)
        self.total_cost_of_loan = attributes.get('totalCostOfLoan', None)
        self.total_waived = attributes.get('totalWaived', None)
        self.total_written_off = attributes.get('totalWrittenOff', None)
        self.total_outstanding = attributes.get('totalOutstanding', None)
        self.total_overdue = attributes.get('totalOverdue', None)
        self.overdue_since_date = self._make_date_object(attributes.get('overdueSinceDate', None))
        self.in_arrears = attributes.get('inArrears', None)
        self.is_npa = attributes.get('isNPA', None)


class LoanRepaymentSchedule(FineractObject):
    """
    This class represents a loan repayment schedule
    """

    def _init_attributes(self):
        self.currency = None
        self.loan_term_in_days = None
        self.total_principal_disbursed = None
        self.total_principal_expected = None
        self.total_principal_paid = None
        self.total_interest_charged = None
        self.total_fee_charges_charged = None
        self.total_penalty_charges_charged = None
        self.total_waived = None
        self.total_written_off = None
        self.total_repayment_expected = None
        self.total_repayment = None
        self.total_outstanding = None
        self.periods = None

    def _use_attributes(self, attributes):
        self.currency = self._make_fineract_object(Currency, attributes.get('currency', None))
        self.loan_term_in_days = attributes.get('loanTermInDays', None)
        self.total_principal_disbursed = attributes.get('totalPrincipalDisbursed', None)
        self.total_principal_expected = attributes.get('totalPrincipalExpected', None)
        self.total_principal_paid = attributes.get('totalPrincipalPaid', None)
        self.total_interest_charged = attributes.get('totalInterestCharged', None)
        self.total_fee_charges_charged = attributes.get('totalFeeChargesCharged', None)
        self.total_penalty_charges_charged = attributes.get('totalPenaltyChargesCharged', None)
        self.total_waived = attributes.get('totalWaived', None)
        self.total_written_off = attributes.get('totalWrittenOff', None)
        self.total_repayment_expected = attributes.get('totalRepaymentExpected', None)
        self.total_repayment = attributes.get('totalRepayment', None)
        self.total_outstanding = attributes.get('totalOutstanding', None)
        self.periods = self._make_fineract_objects_list(LoanRepaymentPeriod, attributes.get('periods', None))


class LoanRepaymentPeriod(FineractObject):

    def _init_attributes(self):
        self.period = None
        self.from_date = None
        self.due_date = None
        self.days_in_period = None
        self.principal_original_due = None
        self.principal_due = None
        self.principal_outstanding = None
        self.principal_disbursed = None
        self.principal_loan_balance = None
        self.principal_loan_balance_outstanding = None
        self.interest_original_due = None
        self.interest_dues = None
        self.interest_outstanding = None
        self.fee_charges_due = None
        self.fee_charges_outstanding = None
        self.penalty_charges_due = None
        self.total_original_due_for_period = None
        self.total_due_for_period = None
        self.total_paid_for_period = None
        self.total_outstanding_for_period = None
        self.total_overdue = None
        self.total_actual_cost_of_loan_for_period = None

    def _use_attributes(self, attributes):
        self.period = attributes.get('period', None)
        self.due_date = self._make_date_object(attributes.get('dueDate', None))
        self.from_date = self._make_date_object(attributes.get('fromDate', None))
        self.days_in_period = attributes.get('daysInPeriod', None)
        self.principal_original_due = attributes.get('principalOriginalDue', None)
        self.principal_due = attributes.get('principalDue', None)
        self.principal_outstanding = attributes.get('principalOutstanding', None)
        self.principal_disbursed = attributes.get('principalDisbursed', None)
        self.principal_loan_balance_outstanding = attributes.get('principalLoanBalanceOutstanding', None)
        self.interest_original_due = attributes.get('interestOriginalDue', None)
        self.interest_due = attributes.get('interestDue', None)
        self.interest_outstanding = attributes.get('interestOutstanding', None)
        self.fee_charges_due = attributes.get('feeChargesDue', None)
        self.fee_charges_outstanding = attributes.get('feeChargesOutstanding', None)
        self.penalty_charges_due = attributes.get('penaltyChargesDue', None)
        self.total_original_due_for_period = attributes.get('totalOriginalDueForPeriod', None)
        self.total_due_for_period = attributes.get('totalDueForPeriod', None)
        self.total_paid_for_period = attributes.get('totalPaidForPeriod', None)
        self.total_outstanding_for_period = attributes.get('totalOutstandingForPeriod', None)
        self.total_overdue = attributes.get('totalOverdue', None)
        self.total_actual_cost_of_loan_for_period = attributes.get('totalActualCostOfLoanForPeriod', None)


class LoanTransaction(FineractObject):
    """
    This class represents a Loan transaction.
    """

    def _init_attributes(self):
        self.id = None
        self.office_id = None
        self.office_name = None
        self.type = None
        self.date = None
        self.currency = None
        self.amount = None
        self.principal_portion = None
        self.interest_portion = None
        self.fee_charges_portion = None
        self.penalty_charges_portion = None
        self.overpayment_portion = None
        self.unrecognized_income_portion = None
        self.outstanding_loan_balance = None
        self.submitted_on_date = None
        self.manually_reversed = None

    def _use_attributes(self, attributes):
        self.id = attributes.get('id', None)
        self.office_id = attributes.get('officeId', None)
        self.office_name = attributes.get('officeName', None)
        self.type = self._make_fineract_object(LoanTransactionType, attributes.get('type', None))
        self.date = self._make_date_object(attributes.get('date', None))
        self.currency = self._make_fineract_object(Currency, attributes.get('currency', None))
        self.amount = attributes.get('amount', None)
        self.principal_portion = attributes.get('principalPortion', None)
        self.interest_portion = attributes.get('interestPortion', None)
        self.fee_charges_portion = attributes.get('feeChargesPortion', None)
        self.penalty_charges_portion = attributes.get('penaltyChargesPortion', None)
        self.overpayment_portion = attributes.get('overpaymentPortion', None)
        self.unrecognized_income_portion = attributes.get('unrecognizedIncomePortion', None)
        self.outstanding_loan_balance = attributes.get('outstandingLoanBalance', None)
        self.submitted_on_date = self._make_date_object(attributes.get('submittedOnDate', None))
        self.manually_reversed = attributes.get('manuallyReversed', None)


class LoanTransactionType(Type):

    def _init_attributes(self):
        super(LoanTransactionType, self)._init_attributes()
        self.disbursement = None
        self.repayment_at_disbursement = None
        self.repayment = None
        self.contra = None
        self.waive_interest = None
        self.waive_charges = None
        self.accrual = None
        self.write_off = None
        self.recovery_payment = None
        self.initiate_transfer = None
        self.approve_transfer = None
        self.withdraw_transfer = None
        self.reject_transfer = None
        self.charge_payment = None
        self.refund = None
        self.refund_for_active_loans = None

    def _use_attributes(self, attributes):
        super(LoanTransactionType, self)._use_attributes(attributes)
        self.disbursement = attributes.get('disbursement', None)
        self.repayment_at_disbursement = attributes.get('repaymentAtDisbursement', None)
        self.repayment = attributes.get('repayment', None)
        self.contra = attributes.get('contra', None)
        self.waive_interest = attributes.get('waiveInterest', None)
        self.waive_charges = attributes.get('waiveCharges', None)
        self.write_off = attributes.get('writeOff', None)
        self.recovery_payment = attributes.get('recoveryPayment', None)
        self.initiate_transfer = attributes.get('initiateTransfer', None)
        self.approve_transfer = attributes.get('approveTransfer', None)
        self.withdraw_transfer = attributes.get('withdrawTransfer', None)
        self.reject_transfer = attributes.get('rejectTransfer', None)
        self.charge_payment = attributes.get('chargePayment', None)
        self.refund = attributes.get('refund', None)
        self.refund_for_active_loans = attributes.get('refundForActiveLoans', None)
