function main(splash, args)
    splash:init_cookies(args.splash_cookies)
    splash.private_mode_enabled = false

    -- Set custom headers
    splash:set_custom_headers({
        ["User-Agent"] = args.headers["User-Agent"],
        ["Referer"] = args.headers["Referer"],
        ["Cookie"] = args.cookies
    })

    -- Navigate to the URL
    splash:go(args.reply_url)
    splash:wait(4)

    -- Focus and click the text box
    local select_contact = splash:jsfunc([[
        function(content) {
            var textBox = document.getElementById('ctl00_mainContentPlaceHolder_addressBox_addressTextBox');
            if (textBox) {
                textBox.focus();
                textBox.click();
                textBox.value = content;
            } else {
                return 'Message text box not found';
            }
        }
    ]])

    select_contact(args.message_content)  -- Pass the content to the function

    splash:wait(1)

    -- Select the checkbox
    local select_contact_textbox = splash:jsfunc([[
        function() {
            var parentElement = document.getElementById("checkbox6");
            if (parentElement) {
                var checkbox = parentElement.querySelector("#ctl00_mainContentPlaceHolder_addressBox_addressGrid_ctl08_sendCheckBox");
                if (checkbox && !checkbox.checked) {
                    checkbox.click();
                    return "Checkbox clicked!";
                } else if (checkbox && checkbox.checked) {
                    return "Checkbox already checked!";
                }
                return "Checkbox not found!";
            } else {
                return "Parent element not found!";
            }
        }
    ]])

    local checkbox_result = select_contact_textbox()
    splash:wait(1)

    -- Simulate the button click and call the onclick method
    local result = splash:evaljs([[
        (function() {
            var okButton = document.getElementById('ctl00_mainContentPlaceHolder_addressBox_okButton');
            if (okButton) {
                // Check if the button has an onclick attribute
                if (okButton.onclick) {
                    // Call the onclick function directly
                    okButton.onclick();
                    return 'onclick function executed';
                } else if (typeof __doPostBack === 'function') {
                    // Fallback to calling __doPostBack if onclick is not defined
                    __doPostBack('ctl00$mainContentPlaceHolder$addressBox$okButton', '');
                    return '__doPostBack executed';
                }
                return 'Button found but no onclick handler';
            }
            return 'Button not found';
        })()
    ]])

    splash:wait(3)  -- Wait for any potential AJAX or postback to complete

    -- Collect results
    local har = splash:har()
    local screenshot = splash:png()
    local html_content = splash:html()

    return {
        html = html_content,
        png = screenshot,
        har = har,
        result = result
    }
end
