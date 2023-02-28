import re
import copy
import modules.scripts as scripts
import modules.processing as processing
import gradio as gr

import modules.shared as shared

from modules.processing import process_images, Processed

verbose_logging = True  # prints the Prompt, Negative prompt, and Seed before each image is generated


def log(string):
    if verbose_logging:
        print(string)


# determines if clicking the orange Generate button will do anything
def is_script_ready(prompt_text):
    return prompt_text != ""


scratch_prompt_textbox = None
scratch_negative_prompt_textbox = None
scratch_seed_textbox = None


class Script(scripts.Script):
    def title(self):
        return "Keep this prompt for later"

    def show(self, is_img2img):
        return not is_img2img  # only show in txt2img. not relevant for img2img

    def after_component(self, component, **kwargs):
        global scratch_prompt_textbox
        global scratch_negative_prompt_textbox
        global scratch_seed_textbox

        #if component.elem_id == "open_folder":
        #if component.elem_id == "txt2img_generation_info_button": #very bottom of the txt2img image gallery
        if component.elem_id == "extras_tab":

            #with gr.Column(scale=1):
            # this button needs to be added after the scripts dropdown somewhere
            keep_this_prompt_for_later_button = gr.Button(value="\u2199\ufe0f Keep this prompt for later",
                                                          elem_id="keep_this_prompt_for_later_button",
                                                          )

            keep_this_prompt_for_later_button.click(fn=None,
                                                    scroll_to_output=False,
                                                    show_progress=False,
                                                    inputs=[],
                                                    outputs=[scratch_prompt_textbox,
                                                             scratch_negative_prompt_textbox,
                                                             scratch_seed_textbox],
                                                    _js="function() { return keep_this_prompt_for_later_button_click() }",
                                                    )

    def ui(self, is_img2img):
        with gr.Row(elem_id="keep_this_prompt_for_later_section"):
            with gr.Column():

                script_ready_html = gr.HTML('<div id="keepthispromptforlater-status" title="Clicking the orange Generate button will render all the prompts in the textbox below">Script status: <span class="ready">Ready!</span></div>',
                                            visible=False,
                                            )
                script_not_ready_html = gr.HTML('<div id="keepthispromptforlater-status" title="At least one prompt must be in the \'Prompts\' textbox in the Prompts tab below for this script to active, until then it does nothing">Script status: <span class="notready">Not ready</span></div>',
                                                visible=True,
                                                )

                with gr.Tab("Prompts", elem_id="keep_this_prompt_for_later_prompt_tab_section"):
                    prompt_textbox = gr.Textbox(label="Prompts",
                                                lines=2,
                                                placeholder="List of prompts (separate with newlines) [required]",
                                                max_lines=4,
                                                elem_id="prompt_textbox",
                                                )

                    def on_prompt_textbox_change(prompt_text):
                        #print(f"prompt_text={prompt_text}")
                        if is_script_ready(prompt_text):
                            return gr.HTML.update(visible=True), gr.HTML.update(visible=False)
                        else:
                            return gr.HTML.update(visible=False), gr.HTML.update(visible=True)

                    prompt_textbox.change(
                        fn=on_prompt_textbox_change,
                        inputs=[prompt_textbox],
                        outputs=[script_ready_html, script_not_ready_html],
                        show_progress=False,
                    )

                    negative_prompt_textbox = gr.Textbox(label="Negative Prompts",
                                                         lines=2,
                                                         placeholder="List of negative prompts (separate with newlines) [optional]",
                                                         max_lines=4,
                                                         elem_id="negative_prompt_textbox",
                                                         )
                    seed_textbox = gr.Textbox(label="Seeds",
                                              lines=2,
                                              placeholder="List of seed values (separate with commas, spaces, or newlines) [optional]",
                                              max_lines=4,
                                              elem_id="seed_textbox",
                                              )

                    with gr.Row():
                        with gr.Column(scale=1, min_width=1):
                            pass
                        with gr.Column(scale=1):
                            pass
                        with gr.Column(scale=1):
                            def clear_main_textboxes():
                                # remove all text in the main tab textboxes
                                return "", "", ""

                            clear_main_textboxes_button = gr.Button(value="Clear these textboxes")
                            clear_main_textboxes_button.click(clear_main_textboxes,
                                                              inputs=[],
                                                              outputs=[prompt_textbox,
                                                                       negative_prompt_textbox,
                                                                       seed_textbox]
                                                              )
                    with gr.Row():
                        ignore_batch_checkbox = gr.Checkbox(value=True,
                                                            label="Ignore batch count/size",
                                                            elem_id="ignore_batch_checkbox",
                                                            )
                        ignore_batch_checkbox.style(container=True)


                with gr.Tab("Scratch paper", elem_id="keep_this_prompt_for_later_scratch_tab_section"):
                    global scratch_prompt_textbox
                    global scratch_negative_prompt_textbox
                    global scratch_seed_textbox

                    scratch_prompt_textbox = gr.Textbox(label="Scratch paper - Prompts",
                                                        placeholder="This textbox is used as temporary storage for prompts",
                                                        lines=2,
                                                        max_lines=4,
                                                        elem_id="scratch_prompt_textbox",
                                                        )
                    scratch_negative_prompt_textbox = gr.Textbox(label="Scratch paper - Negative Prompts",
                                                                 placeholder="This textbox is used as temporary storage for negative prompts",
                                                                 lines=2,
                                                                 max_lines=4,
                                                                 elem_id="scratch_negative_prompt_textbox",
                                                                 )
                    scratch_seed_textbox = gr.Textbox(label="Scratch paper - Seeds",
                                                      placeholder="This textbox is used as temporary storage for seeds",
                                                      lines=2,
                                                      max_lines=4,
                                                      elem_id="scratch_seed_textbox",
                                                      )

                    with gr.Row():
                        # with gr.Column(scale=1, min_width=1):
                        #    pass
                        with gr.Column(scale=1):
                            def copy_textboxes(a, b, c):
                                return a, b, c

                            def clear_scratch_textboxes():
                                # remove all text in the scratch paper textboxes
                                return "", "", ""

                            move_to_other_tab_button = gr.Button(value="Move text to main tab for rendering")
                            move_to_other_tab_button.click(fn=copy_textboxes,
                                                           inputs=[scratch_prompt_textbox,
                                                                   scratch_negative_prompt_textbox,
                                                                   scratch_seed_textbox],
                                                           outputs=[prompt_textbox,
                                                                    negative_prompt_textbox,
                                                                    seed_textbox])
                            move_to_other_tab_button.click(fn=clear_scratch_textboxes,
                                                           inputs=[],
                                                           outputs=[scratch_prompt_textbox,
                                                                    scratch_negative_prompt_textbox,
                                                                    scratch_seed_textbox])
                            move_to_other_tab_button.click(fn=None,
                                                           inputs=[],
                                                           outputs=[scratch_prompt_textbox,
                                                                    scratch_negative_prompt_textbox,
                                                                    scratch_seed_textbox],
                                                           _js="function() { return move_to_other_tab_button_click() }",
                                                           )
                        with gr.Column(scale=2, min_width=1):
                            pass

                with gr.Accordion(label="Keep this prompt for later - Help", open=False):
                    gr.HTML(
                        """
                        <div class="keepthispromptforlater">
                            This script helps you generate batches of images with unique prompts and seeds.
                            <br>
                            <br>This script will only activate when one or more prompts are typed in the Prompts textbox in the Prompts tab.
                            <br>
                            <br>This script adds a "\u2199\ufe0f Keep this prompt for later" button below the image gallery and the full screen image viewer. Read the Workflow section below to learn how it works.
                            <br>
                            <br><hr>
                            <br><h3>Workflow:</h3>
                            <br>After generating images the normal way with low quality settings (ie: 512x512, low step count, non ancestral sampler), select which ones you like in the image gallery and click the new Keep this prompt for later button in the bottom right to copy the prompts/seed into the Scratch paper tab.
                            <br>
                            <br>After you are finished, click the "Move to main tab for rendering" button in the Scratch paper tab to move the text over to the Prompts tab.
                            <br>Now that text is in the Prompts tab, the script is enabled. This is when you can change the image generation settings (ie: 512x512 -> 1024x1024 with Hires fix, higher step count) and click Generate to generate all these images at once with improved quality.
                            <br>
                            <br>After the images are finished generating in a higher quality you can click the "Clear these textboxes" button in the Prompts tab to clear the textboxes to go for another round.
                            <br>
                            <br><hr>
                            <br><h3>Details:</h3>
                            <br>If there are no prompts entered, then images will be generated as normal, as if this script wasn't running.
                            <br>But if there are prompts entered, then each prompts will be generated using the aligned negative prompt and seed.
                            <br>
                            <br>If you decide to enter text manually, and if there are more prompts entered than negative prompts or seeds, then the original negative prompt and/or seed will be used.
                            <br>
                            <br>
                            <br><hr>
                            <br><h3>Example:</h3>
                            <br>For example, lets say you manually entered:
                            <br>
                            <br>Prompts:
                            <ol>
                                <li>a woman</li>
                                <li>a car</li>
                                <li>a house</li>
                            </ol>
                            <br>Negative Prompts:
                            <ol>
                                <li>ugly</li>
                            </ol>
                            <br>Seeds:
                            <ol>
                                <li>123</li>
                                <li>456</li>
                            </ol>
                            <br>Then 3 images would be rendered when clicking Generate:
                            <br>
                            <ol>
                                <li>"a woman" with negative prompt "ugly" and seed "123"</li>
                                <li>"a car" with seed "456"</li>
                                <li>"a house"</li>
                            <ul>
                        </div>
                        """)

        return [prompt_textbox, negative_prompt_textbox, seed_textbox, ignore_batch_checkbox]

    def run(self, p, prompt_textbox, negative_prompt_textbox, seed_textbox, ignore_batch):

        if not is_script_ready(prompt_textbox):
            return  # generate images as if this script isn't activated

        prompts = []
        prompts = re.split("\n", prompt_textbox)  # split by newline

        negative_prompts = []
        negative_prompts = re.split("\n", negative_prompt_textbox)  # split by newline
        if negative_prompts == ['']:
            negative_prompts = []   # edge case when negative_prompt_textbox is empty

        seeds = []
        seeds = re.split(",| |\n", seed_textbox)  # split by comma, space, or newline
        seeds = list(filter(None, seeds))  # filter out any bad data created by multiple separators in the textbox

        if ignore_batch:
            p.n_iter = 1  # override users 'Batch count'
            p.batch_size = 1  # override users 'Batch size'
        p.all_seeds = seeds

        original_seed = p.seed
        original_negative_prompt = p.negative_prompt

        total_image_count = len(prompts) * p.n_iter * p.batch_size
        step_count = p.steps * total_image_count
        batched_text = ""
        hires_text_job = ""
        hires_text_steps = ""
        if p.enable_hr:
            step_count = (p.steps + p.hr_second_pass_steps) * total_image_count
            #step_count *= 2
            hires_text_job = f"({total_image_count * 2} jobs with Hires fix) "
            hires_text_steps = f" ({p.steps * total_image_count} normal, {p.hr_second_pass_steps * total_image_count} Hires)"
        if p.batch_size > 1:
            #step_count = p.steps * total_image_count
            batched_text = f"({int(step_count / p.batch_size)} batched) "
        print(f"[Keep this prompt for later]: Will create {total_image_count} images {hires_text_job}over {int(step_count)} {batched_text}steps{hires_text_steps}")

        # print(f"len(prompts)={len(prompts)}")
        # print(f"p.n_iter={p.n_iter}")
        # print(f"p.batch_size={p.batch_size}")
        # print(f"p.steps={p.steps}")
        # print(f"p.hr_second_pass_steps={p.hr_second_pass_steps}")
        # print(f"total_image_count={total_image_count}")
        # print(f"step_count={step_count}")
        # print(f"shared.state.job_count (start)={shared.state.job_count}")
        # print(f"shared.state.job_no (start)={shared.state.job_no}")
        # print(f"shared.state.sampling_step={shared.state.sampling_step}")
        # print(f"shared.state.sampling_steps={shared.state.sampling_steps}")


        all_prompts = []
        all_negative_prompts = []
        all_seeds = []
        images_list = []
        i = 0
        for prompt in prompts:
            # print(f"shared.state.job_count (in loop)={shared.state.job_count}")
            # print(f"shared.state.job_no (in loop)={shared.state.job_no}")

            #this fixes the progress bar in the UI, but the console stops at 50%
            # if p.enable_hr:
            #     shared.state.job_count = p.n_iter * len(prompts) * 2
            #     #print(f"[KEEP THIS PROMPT FOR LATER] shared.state.job_count={shared.state.job_count} with hires")
            # else:
            #     shared.state.job_count = p.n_iter * len(prompts)
            #     #print(f"[KEEP THIS PROMPT FOR LATER] shared.state.job_count={shared.state.job_count}")

            shared.state.job_count = p.n_iter * len(prompts)  # used to fix the progress bar, but is broken now. UI reaches 100% when only 50% is done.
            #shared.state.processing_has_refined_job_count = True # TESTING 1/27

            log(f"\nPrompt: {prompt}")
            if i < len(negative_prompts):
                negative_prompt = negative_prompts[i]
                log(f"Negative Prompt: {negative_prompt}")
            else:
                negative_prompt = original_negative_prompt

            if i < len(seeds):
                seed = seeds[i].strip()
                log(f"Seed: {seed}")
                # print(f"Seed from seeds[{i}]: [{seed}]\n")
            else:
                seed = processing.get_fixed_seed(original_seed)  # gets a random seed if -1, '', or None
                seeds.append(seed)
                # print(f"Seed (from original_seed): [{seed}]\n")

            j = 0
            for a in range(p.batch_size):
                for b in range(p.n_iter):
                    all_prompts.append(prompt)
                    all_negative_prompts.append(negative_prompt)
                    all_seeds.append(str(int(seed) + j))
                    j += 1

            p.prompt = prompt
            p.negative_prompts = negative_prompt
            p.seed = seed
            proc = process_images(p)
            images_list += proc.images
            i += 1

        info_text = f"Keep this prompt for later - {len(images_list)} images"
        print(f"\n[Keep this prompt for later] Finished creating {len(images_list)} images.")

        return Processed(p, images_list, all_seeds[0], info_text, None, all_prompts, all_negative_prompts, all_seeds, None, 0, None)
        # return Processed(p, images_list, seeds[0], info_text, None, prompts, negative_prompts, seeds, None, 0, None)
        # (p: StableDiffusionProcessing, images_list, seed=-1, info="", subseed=None, all_prompts=None, all_negative_prompts=None, all_seeds=None, all_subseeds=None, index_of_first_image=0, infotexts=None)
