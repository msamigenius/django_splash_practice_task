

function main(splash, args)
    splash:init_cookies(args.splash_cookies)

    splash.private_mode_enabled = false

    -- below lines are setting the headers inside the splash browser window.
    splash:set_custom_headers({
        ["User-Agent"] = args.headers["User-Agent"],
        ["Referer"] = args.headers["Referer"],
        ["Cookie"] = args.cookies
    })

    -- Start capturing HAR data
    -- splash:har_start()

    -- below lines are opening the sent reply_url in the post request
    -- in the splash browser window
    splash:go(args.reply_url)
    splash:wait(4)
 
    -- Capture the screenshot in PNG format









    



    local select_contact = splash:jsfunc([[
        function(content) {
            var textBox = document.getElementById('ctl00_mainContentPlaceHolder_addressBox_addressTextBox');
            if (textBox) {
                textBox.focus(); 
                textBox.click(); // Focus on the textarea to simulate user interaction
                textBox.value = content;  // Clear existing content
            } else {
                return 'Message text box not found';
            }
        }
    ]])
    
    select_contact()


    splash:wait(1)


    -- Function to select the checkbox
    local select_contact_textbox = splash:jsfunc([[
        function() {
        var parentElement = document.getElementById("checkbox6");
        if (parentElement) {
            var checkbox = parentElement.querySelector("#ctl00_mainContentPlaceHolder_addressBox_addressGrid_ctl08_sendCheckBox");
            if (checkbox && !checkbox.checked) {
            checkbox.click();
            return "Checkbox clicked!";
        }   else if (checkbox && checkbox.checked) {
            return "Checkbox already checked!";
        }
            return "Checkbox not found!";
      }     else {
            return "Parent element not found!";
      }
    }
  ]])
    select_contact_textbox()

    local function clickOkButton()
        local okButton = splash:select('#ctl00_mainContentPlaceHolder_addressBox_okButton')

        if okButton then
            okButton:mouse_click()
            okButton:mouse_click()
        -- splash:send_keys("<Enter>")
            splash:wait(3)
  
            if splash:evaljs("typeof(__doPostBack) === 'function'") then
                splash:evaljs("__doPostBack('ctl00$mainContentPlaceHolder$addressBox$okButton','')")
                splash:wait(5)  -- Wait a bit longer for postback to complete
            end
  
            return true
        else
            return false
     end
    end

-- Execute the OK button click function
    local ok_button_result = clickOkButton()





    
    


    -- local select_first_checkbox = splash:jsfunc([[
    --     function() {
    --         // Get the list of all checkboxes on the page
    --         var checkboxes = document.querySelectorAll('ctl00_mainContentPlaceHolder_addressBox_addressGrid_ctl02_sendCheckBox');
    
    --         // Check if any checkbox is found
    --         if (checkboxes.length > 0) {
    --             var firstCheckbox = checkboxes[0];  // Select the first checkbox
    --             firstCheckbox.click();  // Simulate clicking the first checkbox
    --             return 'First checkbox clicked';
    --         } else {
    --             return 'No checkboxes found on the page';
    --         }
    --     }
    -- ]])
    -- select_first_checkbox()

    -- local select_contact_textbox = splash:jsfunc([[
    --     function(content) {
    --     var parentElement = document.getElementById("checkbox6");
    --     if (parentElement) {
    --         var checkbox = parentElement.querySelector("#ctl00_mainContentPlaceHolder_addressBox_addressGrid_ctl08_sendCheckBox");
    --         if (checkbox && !checkbox.checked) {
    --             checkbox.click();
    --             return "Checkbox clicked!";
    --         } else if (checkbox.checked) {
    --             return "Checkbox already checked!";
    --         }
    --         return "Checkbox not found!";
    --     } else {
    --         return "Parent element not found!";
    --     }
    --     }
    -- ]])
    
    
    -- select_contact_textbox()


    -- splash:wait(2)
    -- -- local result = splash:evaljs([[
    -- --     (function() {
    -- --         // Define the __doPostBack function if not already defined
    -- --         if (typeof __doPostBack === 'undefined') {
    -- --             console.error("__doPostBack function is not defined on this page.");
    -- --             return false;
    -- --         }

    -- --         // Invoke the __doPostBack function with the correct parameters
    -- --         __doPostBack('ctl00$mainContentPlaceHolder$addressBox$okButton', '');
    -- --         return true;
    -- --     })()
    -- -- ]])

    --    -- --Ok button --  
    -- local click_clear_button = splash:jsfunc([[
    --     function() {
    --         var button = document.getElementById('ctl00_mainContentPlaceHolder_addressBox_okButton');
    --         if (button && button.value === 'OK') {
    --             button.click();
    --             button.dispatchEvent(new Event('click'));

    --             return "Button clicked!";
    --         } else if (button) {
    --             return "Button found but value is not 'OK'.";
    --         } else {
    --             return "Button not found!";
    --         }
    --     }
    -- ]])
    -- -- splash:wait(3)
    -- result = click_clear_button()


    -- local check_and_click_button = splash:jsfunc([[
    --     function() {
    --         // Find the input button by its ID and value
    --         var button = document.querySelector('input#ctl00_mainContentPlaceHolder_addressBox_okButton.btn.small[type="button"]');
    --         if (button && button.value === 'OK') {
    --             // Click the button
    --             button.click();
    --             button.dispatchEvent(new Event('click'));
    --             return "OK Button clicked!";
    --         } else if (button) {
    --             return "Button found but value is not 'OK'.";
    --         } else {
    --             return "Button not found.";
    --         }
    --     }
    -- ]])

    -- -- Execute the JavaScript function
    -- local result = check_and_click_button()
-- Define a function to perform actions on a web page
--     function perform_actions_on_page()
--     -- Navigate to the target URL
--  -- Wait for the page to load

--     -- Get the button element by its ID
--         local button = splash:select("#ctl00_mainContentPlaceHolder_addressBox_okButton")

--     -- Check if the button is found
--         if button then
--         -- Simulate a click on the button
--             button:click()
        
--         -- Wait for the page to process the click
--             splash:wait(3)

--         else
--             return { error = "Button not found" }
--         end
--     end


--     perform_actions_on_page()
    

    




    local enter_subject_textbox = splash:jsfunc([[
        function(content) {
            var textBox = document.getElementById('ctl00_mainContentPlaceHolder_subjectTextBox');
            if (textBox) {
                textBox.focus();  // Focus on the textarea to simulate user interaction
                textBox.value = content;  // Clear existing content
            } else {
                return 'Message text box not found';
            }
        }
    ]])

        --    -- below line calls the above function
    enter_subject_textbox(args.subject_content)
    splash:wait(1)

    


    -- --    -- below line calls the above function
    -- -- enter_subject_textbox(args.subject_content)


    -- -- this message was sent in the post request.
    local enter_message_textbox = splash:jsfunc([[
        function(content) {
            var textBox = document.getElementById('ctl00_mainContentPlaceHolder_messageTextBox');
            if (textBox) {
                textBox.focus();  // Focus on the textarea to simulate user interaction
                textBox.value = content;  // Clear existing content
            } else {
                return 'Message text box not found';
            }
        }
    ]])
    -- below line calls the above function
    enter_message_textbox(args.message_content)

    splash:wait(1)
    
    


    -- -- local trigger_postback = splash:jsfunc([[
    -- --     function() {
    -- --         var button = document.getElementById("ctl00_mainContentPlaceHolder_addressBox_okButton");
    -- --         if (button) {
    -- --             __doPostBack('ctl00$mainContentPlaceHolder$addressBox$okButton', ''); // trigger postback
    -- --             return "Postback triggered!";
    -- --         } else {
    -- --             return "Button not found!";
    -- --         }
    -- --     }
    -- -- ]])

    -- -- -- Execute the JavaScript function to trigger the postback
    -- -- local result = trigger_postback()



    -- -- -- below line maximizes the splash browser window
 
       --Ok button --  
    local submit_form = splash:jsfunc([[
        function() {

            var submitButton = document.getElementById('ctl00_mainContentPlaceHolder_saveButton');
            if (submitButton) {
                submitButton.dispatchEvent(new Event('click'));
                return "send message ";
            } else {
                console.error('Submit button not found');
                return "Submit button not found";
            }
        }
    ]])

    result=submit_form()

    splash:wait(10)
    local har = splash:har()
    local screenshot = splash:png()
    -- local har_data = splash:har_stop()
    

    -- Get the HTML content of the page
    local html_content = splash:html()
    

    -- Return both the screenshot and HTML content
    return {
        html = html_content,
        png = screenshot,
        har=har,
        result=result
        
    }



end