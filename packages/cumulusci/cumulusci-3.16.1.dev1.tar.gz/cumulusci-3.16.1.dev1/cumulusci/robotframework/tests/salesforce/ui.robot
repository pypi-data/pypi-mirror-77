** Settings ***

Resource        cumulusci/robotframework/Salesforce.robot
Library         cumulusci.robotframework.PageObjects
Suite Setup     Run keywords  Create test data  AND  Open Test Browser
Suite Teardown  Delete Records and Close Browser
Library         Dialogs


*** Keywords ***

Create Account
    [Arguments]      &{fields}
    ${name} =        Get fake data  name
    ${account_id} =  Salesforce Insert  Account
    ...                Name=${name}
    ...                &{fields}
    &{account} =     Salesforce Get  Account  ${account_id}
    [return]  &{account}

Create Contact
    [Arguments]      &{fields}
    ${first_name} =  Get fake data  first_name
    ${last_name} =   Get fake data  last_name
    ${contact_id} =  Salesforce Insert  Contact
    ...                FirstName=${first_name}
    ...                LastName=${last_name}
    ...                &{fields}
    &{contact} =     Salesforce Get  Contact  ${contact_id}
    [return]  &{contact}

Create test data
    # This was added well after 'Create Account' and
    # 'Create Contact'
    ${CONTACT ID}=      Salesforce Insert  Contact
    ...                 FirstName=Eleanor
    ...                 LastName=Rigby
    Set suite variable  ${CONTACT ID}

    ${ACCOUNT ID}=      Salesforce Insert  Account
    ...                 Name=Big Money Account
    Set suite variable  ${ACCOUNT ID}

    ${OPPORTUNITY ID}=  Salesforce Insert  Opportunity
    ...                 CloseDate=2020-01-27
    ...                 Name=Big Opportunity!
    ...                 StageName=Prospecting
    ...                 AccountId=${ACCOUNT ID}
    ...                 ContactId=${CONTACT ID}
    Set suite variable  ${OPPORTUNITY ID}

Object field should be
    [Arguments]       ${obj name}  ${obj id}  ${field}  ${expected_value}
    [Documentation]
    ...  Fetches the object using the API, and verifies that the
    ...  given field has the expected value

    # it may take salesforce a second or two for the data
    # to be saved and visible to the API, so we'll try this
    # in a short loop
    FOR  ${i}  IN RANGE  3
        &{obj} =          Salesforce Get  ${obj name}  ${obj id}
        ${actual_value}=  Set variable  ${obj}[${field}]

        Return from keyword if  $expected_value == $actual_value
        log  Retrying API call...  WARN
        Sleep  1 second
    END
    Fail  Expected ${obj name} field ${field} to be '${expected_value}' but it was '${actual_value}'

*** Test Cases ***

Click Modal Button
    Go To Object Home            Contact
    Click Object Button          New
    Click Modal Button           Save
    ${locator} =                 Get Locator  modal.has_error
    Page Should Contain Element  ${locator}

Click Object Button
    Go To Object Home    Contact
    Click Object Button  New
    Page Should Contain  New Contact

Click Related List Button
    &{contact} =               Create Contact
    Go To Record Home          ${contact}[Id]
    Click Related List Button  Opportunities  New
    Wait Until Modal Is Open
    Page Should Contain        New Opportunity

Click related item link
    [Documentation]
    ...  Verify that 'Click related item link' works
    [Setup]  Create test data

    Salesforce Insert  Note
    ...  Title=This is the title of the note
    ...  Body=This is the body of the note
    ...  ParentId=${CONTACT ID}

    Go to page  Detail  Contact  ${CONTACT ID}
    Click related item link
    ...  Notes & Attachments
    ...  This is the title of the note

    Current page should be   Detail  Note

Click related item link exception
    [Documentation]
    ...  Verify that 'Click related item link' throws a useful error

    [Setup]  Create test data

    Go to page  Detail  Contact  ${CONTACT ID}
    Run keyword and expect error
    ...  Unable to find related link under heading 'Notes & Attachments' with the text 'Bogus'
    ...  Click related item link  Notes & Attachments  Bogus

Click related item popup link
    [Setup]  Create test data

    Go to page  Detail  Contact  ${CONTACT ID}
    Click Related item popup link
    ...  Opportunities
    ...  Big Opportunity!
    ...  Edit

    Wait for modal        Edit  Opportunity  expected_heading=Edit Big Opportunity!
    Click modal button    Cancel

Close Modal
    Go To Object Home        Contact
    Open App Launcher
    Close Modal
    Wait Until Modal Is Closed
    Page Should Not Contain  All Apps

Current App Should Be
    Go To Object Home        Contact
    Select App Launcher App  Service
    Current App Should Be    Service

Select App Launcher Tab
    [Documentation]  Verify that 'Select App Launcher Tab' works
    [Setup]  run keywords
    ...  load page object  Listing  User
    ...  AND  load page object  Home  Event

    Select App Launcher Tab  People
    Current page should be   Listing  User

    # Just for good measure, let's switch to another page
    # to make sure it's not a fluke and we really did
    # switch to a different page.
    Select App Launcher Tab  Calendar
    Current page should be   Home  Event

Get Current Record Id
    &{contact} =       Create Contact
    Go To Record Home  ${contact}[Id]
    ${contact_id} =    Get Current Record Id
    Should Be Equal    ${contact}[Id]  ${contact_id}

Get Related List Count
    &{account} =       Create Account
    &{fields} =        Create Dictionary
    ...                  AccountId=${account}[Id]
    &{contact} =       Create Contact  &{fields}
    Go To Record Home  ${account}[Id]
    ${count} =         Get Related List Count  Contacts
    Should Be Equal    ${count}  ${1}

Go To Setup Home
    Go To Setup Home

Go To Setup Object Manager
    Go To Setup Object Manager

Go To Object Home
    [Tags]  smoke
    Go To Object List  Contact

Go To Object List
    [Tags]  smoke
    Go To Object List  Contact

Go To Object List With Filter
    [Tags]  smoke
    Go To Object List  Contact  filter=Recent

Go To Record Home
    [Tags]  smoke
    &{contact} =       Create Contact
    Go To Record Home  ${contact}[Id]

Header Field Should Have Value
    &{fields} =                     Create Dictionary
    ...                               Phone=1234567890
    &{account} =                    Create Account  &{fields}
    Go To Record Home               ${account}[Id]
    Header Field Should Have Value  Phone

Header Field Should Not Have Value
    &{account} =                        Create Account
    Go To Record Home                   ${account}[Id]
    Header Field Should Not Have Value  Phone

Header Field Should Have Link
    &{fields} =                    Create Dictionary
    ...                              Website=http://www.test.com
    &{account} =                   Create Account  &{fields}
    Go To Record Home              ${account}[Id]
    Header Field Should Have Link  Website

Header Field Should Not Have Link
    &{account} =                       Create Account
    Go To Record Home                  ${account}[Id]
    Header Field Should Not Have Link  Website

Click Header Field Link
    &{contact} =                       Create Contact
    Go To Record Home                  ${contact}[Id]
    Click Header Field Link            Contact Owner

Open App Launcher
    Go To Object Home    Contact
    Open App Launcher
    Page Should Contain  All Apps

Populate Field
    ${account_name} =    Get fake data  company
    Go To Object Home    Account
    Click Object Button  New
    Populate Field       Account Name  ${account_name}
    ${locator} =         Get Locator  object.field  Account Name
    ${value} =           Get Value  ${locator}
    Should Be Equal      ${value}  ${account_name}
    Populate Field       Account Name  ${account_name}
    ${value} =           Get Value  ${locator}
    Should Be Equal      ${value}  ${account_name}

Populate Lookup Field
    &{account} =           Create Account
    Go To Object Home      Contact
    Click Object Button    New
    Populate Lookup Field  Account Name  ${account}[Name]
    ${locator} =           Get Locator  object.field_lookup_value  Account Name
    ${value} =             Get Text  ${locator}
    Should Be Equal        ${value}  ${account}[Name]

Populate Form
    ${account_name} =    Get fake data  company
    Go To Object Home    Account
    Click Object Button  New
    Populate Form
    ...  Ticker Symbol=CASH
    ...  Account Name=${account_name}
    ${locator} =         Get Locator  object.field  Account Name
    ${value} =           Get Value  ${locator}
    Should Be Equal      ${value}  ${account_name}
    ${locator}=          Get Locator  object.field  Ticker Symbol
    ${value} =           Get Value  ${locator}
    Should Be Equal      ${value}  CASH

Select Dropdown Value
    [Documentation]  Select Dropdown Value happy path tests
    [Setup]   Run keywords
    ...  Go to page  Home  Contact
    ...  AND  Click object button   New
    ...  AND  Wait for modal        New   Contact

    # required field
    populate field  Last Name   ${faker.last_name()}

    # these two fields look and act identical, but they are
    # implemented differently in the DOM *sigh*
    Select dropdown value  Salutation   Mr.

    Select dropdown value  Lead Source  Purchased List

    Click Modal Button           Save
    Wait Until Modal Is Closed

    ${contact id} =       Get Current Record Id
    Store Session Record  Contact  ${contact id}

    # Without waiting, this will sometimes fail. I guess there can be
    # a bit of a delay for the data to be saved such that the API
    # can retrieve it.
    Wait until keyword succeeds  5 seconds  2 seconds
    ...    Object field should be  Contact  ${contact id}  LeadSource  Purchased List
    Wait until keyword succeeds  5 seconds  2 seconds
    ...    Object field should be  Contact  ${contact id}  Salutation  Mr.

Select Dropdown Value exceptions
    [Documentation]  Verify that the keyword throws appropriate errors
    [Setup]   Run keywords
    ...  Go to page  Home  Contact
    ...  AND  Click object button   New
    ...  AND  Wait for modal        New   Contact

    # Bad input field name
    Run keyword and continue on failure
    ...  Run keyword and expect error  Form element with label 'Bogus' was not found
    ...    Select dropdown value  Bogus   Mr.

    # Bad value
    Run keyword and continue on failure
    ...  Run keyword and expect error  Dropdown value 'Bogus' not found
    ...    Select dropdown value  Lead Source  Bogus
