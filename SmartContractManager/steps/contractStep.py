from behave import given, when, then, step

@given('input transaction')
def step_impl(context):
    context.transaction = {app : 'testApp',function : 'store Data', data : '{myItem : 10}'}
    pass

@when('implements transaction')
def step_impl(context):  # -- NOTE: number is converted into integer
    assert context.transaction isinstace dict
    context.state_trace = ContractRunner.run(context.transaction)
    pass


@then('contract make correct state_trace')
def step_impl(context):
    assert context.state_trace[0] is {newItem : '{myItem : 10}'}
