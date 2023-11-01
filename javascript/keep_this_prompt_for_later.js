const SCRIPT_NAME = "Keep this prompt for later"    //this should match SCRIPT_TITLE in the python code

document.addEventListener("DOMContentLoaded", function() {
	//inject our button into the fullscreen image viewer
    KeepThisPromptForLater_AddFullscreenButton()
}, false)


function KeepThisPromptForLater_AddFullscreenButton() { //similar to imageviewer.js:189 DOMContentLoaded event listener
	//console.log("KeepThisPromptForLater_AddFullscreenButton()")

	//const modalControls = gradioApp().querySelector("div.modalControls")  //this stopped working after a March update
	const modalControls = document.querySelector("div.modalControls")
	//console.log("modalControls="+modalControls)
	
    const modalButton = document.createElement("span")
    modalButton.className = "modalSave cursor"
    modalButton.id = "KeepThisPromptForLaterFullscreenButton"
    modalButton.innerHTML = "↙️ Keep this prompt for later"
    modalButton.addEventListener("click", KeepThisPromptForLaterFullscreenButton_Click, true)
    modalButton.title = "[Extension] " + SCRIPT_NAME + " (hotkey = Enter)"
    modalButton.style = "grid-area:auto; width:max-content;"	//width:max-content is to make it work with the Image Browser extension

    //modalControls.appendChild(modalButton)
    //insert before the close button
    const modalClose = document.querySelector("span.modalClose")
    modalControls.insertBefore(modalButton, modalClose);

	
	const modal = gradioApp().getElementById("lightboxModal")
	modal.addEventListener('keydown', KeepThisPromptForLater_modalKeyHandler, true)
	
	//console.log("KeepThisPromptForLater_AddFullscreenButton() done")
}

function KeepThisPromptForLaterFullscreenButton_Click(event) {
	//console.log("KeepThisPromptForLaterFullscreenButton_Click()")
	event.stopPropagation() //stops the fullscreen view from closing when clicked
	KeepThisPromptForLater_ClickButton()
}

function KeepThisPromptForLater_modalKeyHandler(event) {
	//console.log("KeepThisPromptForLater_modalKeyHandler()")
	//console.log("event.key="+event.key)
    switch (event.key) {
        case "Enter":
            KeepThisPromptForLater_ClickButton()
            break
    }
}

function KeepThisPromptForLater_ClickButton() {
	gradioApp().getElementById('script_keep_this_prompt_for_later_button').click() //need to do click() so the python code runs too
}

function move_to_other_tab_button_click() {
    //select the "Prompts" tab after clicking this button
    let promptsTab = gradioApp().querySelector("#keep_this_prompt_for_later_section > div > div.tabs > div").firstElementChild
    promptsTab.click()
}

function keep_this_prompt_for_later_button_click() {
	//console.log("keep_this_prompt_for_later_button_click()")

    //let jsonText = gradioApp().querySelector("#tab_txt2img div.gr-form.overflow-hidden > div[class~='!hidden'] > label > textarea").value //old
    let jsonText = gradioApp().querySelector("#generation_info_txt2img > label > textarea").value
    //console.log("jsonText = "+jsonText)

    if (jsonText == "") {
        //No image has been generated yet
        //or we couldn't find the right text box because an update in A1111 changed it
        console.log(SCRIPT_NAME + ": [ERROR] No generation info found for image.")
        return null
    }

    let gen_info = JSON.parse(jsonText)
    //console.log(JSON.stringify(gen_info, null, 4))

    let all_seeds = gen_info["all_seeds"]
    //console.log("all_seeds = "+all_seeds)

    let selectedIndex = selected_gallery_index()
    //console.log("selectedIndex = "+selectedIndex)

    let index = 0
    if (selectedIndex == -1) { //no image selected in gallery
        index = 0
    }
    else {
        index = selectedIndex - gen_info["index_of_first_image"]    //"index_of_first_image" is 1 if an image grid is shown, otherwise 0
    }
    let prompt = gen_info["all_prompts"][index]
    let negative_prompt = gen_info["all_negative_prompts"][index]
    let seed = gen_info["all_seeds"][index]
    //console.log("index="+index)
    //console.log("prompt="+prompt)
    //console.log("negative_prompt="+negative_prompt)
    //console.log("seed="+seed)

    let scratch_prompt_text = gradioApp().querySelector('#script_keep_this_prompt_for_later_prompt_textbox textarea').value;
    let scratch_negative_prompt_text = gradioApp().querySelector('#script_keep_this_prompt_for_later_negative_prompt_textbox textarea').value;
    let scratch_seed_text = gradioApp().querySelector('#script_keep_this_prompt_for_later_seed_textbox textarea').value;


    let new_scratch_prompt_text = scratch_prompt_text + "\n" + prompt
    if (scratch_prompt_text == "") {
        if (prompt == "") {
            new_scratch_prompt_text = " "
        }
        else {
            new_scratch_prompt_text = prompt
        }
    }
    let new_scratch_negative_prompt_text = scratch_negative_prompt_text + "\n" + negative_prompt
    if (scratch_negative_prompt_text == "") {
        if (negative_prompt == "") {
            new_scratch_negative_prompt_text = " "
        }
        else {
            new_scratch_negative_prompt_text = negative_prompt
        }
    }
    let new_scratch_seed_text = scratch_seed_text + " " + seed
    if (scratch_seed_text == "") {
        new_scratch_seed_text = seed
    }

    return [new_scratch_prompt_text, new_scratch_negative_prompt_text, new_scratch_seed_text]
}