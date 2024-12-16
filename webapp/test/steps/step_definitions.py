from behave import given, when, then

@given('the user navigates to the "Generate Use Case Diagram" page')
def step_impl(context):
    context.driver.get("http://localhost:8000/UseCaseDiagram")


@given('the user enters a valid actor name "{actor_name}"')
def step_impl(context, actor_name):
    # Simulasi memasukkan nama aktor ke dalam form
    context.driver.find_element("id", "actor_field").send_keys(actor_name)

@given('the user enters a valid feature name "{feature_name}"')
def step_impl(context, feature_name):
    # Simulasi memasukkan nama fitur ke dalam form
    context.driver.find_element("id", "feature_field").send_keys(feature_name)

@given('the user leaves the actor name field empty')
def step_impl(context):
    # Simulasi membiarkan kolom nama aktor kosong
    context.driver.find_element("id", "actor_field").clear()

@given('the user leaves the feature name field empty')
def step_impl(context):
    # Simulasi membiarkan kolom nama fitur kosong
    context.driver.find_element("id", "feature_field").clear()

@when('the user clicks the "Generate" button')
def step_impl(context):
    # Simulasi menekan tombol "Generate"
    context.driver.find_element("id", "generate_button").click()

@then('the user should see a success message "{message}"')
def step_impl(context, message):
    # Verifikasi pesan sukses
    success_message = context.driver.find_element("id", "success_message").text
    assert success_message == message, f"Expected: {message}, but got: {success_message}"

@then('the user should see an error message "{error_message}"')
def step_impl(context, error_message):
    # Verifikasi pesan error
    error_message_displayed = context.driver.find_element("id", "error_message").text
    assert error_message_displayed == error_message, f"Expected: {error_message}, but got: {error_message}"

@then('the user should be navigated to the "Output Use Case Diagram" page')
def step_impl(context):
    # Verifikasi navigasi ke halaman output
    assert context.driver.current_url == "http://localhost:8000/use_case_result"
