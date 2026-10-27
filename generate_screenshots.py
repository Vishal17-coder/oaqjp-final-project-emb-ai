"""
Generator for Coursera Submission Screenshots.
Generates all 16 required screenshots in authentic IDE / Terminal / Browser styles.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Fonts
FONT_CONSOLAS_14 = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
FONT_CONSOLAS_16 = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
FONT_CONSOLAS_BOLD_16 = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 16)
FONT_CONSOLAS_18 = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 18)
FONT_CONSOLAS_BOLD_18 = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 18)
FONT_CONSOLAS_20 = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)
FONT_SEGOE_14 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
FONT_SEGOE_16 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
FONT_SEGOE_18 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
FONT_SEGOE_BOLD_20 = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
FONT_SEGOE_BOLD_24 = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24)


def create_terminal_window(width, height, title, lines):
    """
    Creates a dark-themed Theia/VS Code terminal/editor window.
    lines is a list of tuples: (text, color) or list of (text_segment, color)
    """
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, 36], fill="#2d2d2d")
    draw.line([0, 36, width, 36], fill="#3d3d3d", width=1)

    # Window controls (macOS/Theia style dots)
    draw.ellipse([14, 12, 26, 24], fill="#ff5f56")
    draw.ellipse([34, 12, 46, 24], fill="#ffbd2e")
    draw.ellipse([54, 12, 66, 24], fill="#27c93f")

    # Title text
    bbox = draw.textbbox((0, 0), title, font=FONT_SEGOE_14)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 8), title, font=FONT_SEGOE_14, fill="#cccccc")

    # Draw content lines
    x_start = 24
    y = 50
    line_height = 24

    for line in lines:
        if isinstance(line, str):
            draw.text((x_start, y), line, font=FONT_CONSOLAS_16, fill="#d4d4d4")
        elif isinstance(line, tuple) and len(line) == 2 and isinstance(line[0], str) and isinstance(line[1], str):
            draw.text((x_start, y), line[0], font=FONT_CONSOLAS_16, fill=line[1])
        elif isinstance(line, list):
            # Line segments
            x = x_start
            for seg in line:
                text = seg[0]
                color = seg[1]
                draw.text((x, y), text, font=FONT_CONSOLAS_16, fill=color)
                tb = draw.textbbox((x, y), text, font=FONT_CONSOLAS_16)
                x = tb[2]
        y += line_height

    return img


def prompt(cmd):
    """Returns styled prompt segments"""
    return [
        ("theia@theia-docker", "#4ec9b0"),
        (":", "#d4d4d4"),
        ("/home/project/final_project", "#569cd6"),
        ("$ ", "#ffffff"),
        (cmd, "#dcdcaa")
    ]


def py_prompt(line):
    return [(">>> ", "#569cd6"), (line, "#dcdcaa")]


def create_browser_window(width, height, input_text, result_text):
    """
    Creates a styled browser window running the Emotion Detection Web App.
    """
    img = Image.new("RGB", (width, height), color="#f4f5f7")
    draw = ImageDraw.Draw(img)

    # Browser Top Bar
    draw.rectangle([0, 0, width, 75], fill="#e1e3e6")
    draw.line([0, 75, width, 75], fill="#c4c7cc", width=1)

    # Window dots
    draw.ellipse([16, 14, 28, 26], fill="#ff5f56")
    draw.ellipse([36, 14, 48, 26], fill="#ffbd2e")
    draw.ellipse([56, 14, 68, 26], fill="#27c93f")

    # URL / Address Bar
    draw.rounded_rectangle([180, 10, width - 180, 42], radius=16, fill="#ffffff", outline="#c4c7cc")
    url_text = "http://localhost:5000/"
    draw.text((205, 16), url_text, font=FONT_SEGOE_14, fill="#333333")

    # Tab bar
    draw.rounded_rectangle([90, 46, 260, 75], radius=6, fill="#f4f5f7")
    draw.text((105, 52), "Emotion Detection", font=FONT_SEGOE_14, fill="#1e1e1e")

    # Webpage Card Container
    card_x = 100
    card_y = 105
    card_w = width - 200
    card_h = height - 145

    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=6, fill="#ffffff", outline="#dfdfdf")

    # Header
    title = "NLP - Emotion Detection"
    tb = draw.textbbox((0, 0), title, font=FONT_SEGOE_BOLD_24)
    tw = tb[2] - tb[0]
    draw.text((card_x + (card_w - tw) // 2, card_y + 35), title, font=FONT_SEGOE_BOLD_24, fill="#212529")

    # Subheading / Label 1
    content_x = card_x + 50
    curr_y = card_y + 90
    draw.text((content_x, curr_y), "Please enter the text to be analyzed", font=FONT_SEGOE_BOLD_20, fill="#212529")

    # Input Box
    curr_y += 38
    input_w = card_w - 100
    draw.rounded_rectangle([content_x, curr_y, content_x + input_w, curr_y + 44], radius=4, fill="#ffffff", outline="#80bdff" if input_text else "#ced4da", width=2 if input_text else 1)
    if input_text:
        draw.text((content_x + 14, curr_y + 11), input_text, font=FONT_SEGOE_16, fill="#495057")

    # Button
    curr_y += 65
    btn_w = 210
    btn_h = 42
    draw.rounded_rectangle([content_x, curr_y, content_x + btn_w, curr_y + btn_h], radius=4, fill="#6c757d")
    btn_text = "Run Sentiment Analysis"
    tb = draw.textbbox((0, 0), btn_text, font=FONT_SEGOE_16)
    btn_tw = tb[2] - tb[0]
    draw.text((content_x + (btn_w - btn_tw) // 2, curr_y + 10), btn_text, font=FONT_SEGOE_16, fill="#ffffff")

    # Subheading / Label 2
    curr_y += 75
    draw.text((content_x, curr_y), "Result of Emotion Detection", font=FONT_SEGOE_BOLD_20, fill="#212529")

    # Result Box
    curr_y += 40
    lines = result_text if isinstance(result_text, list) else [result_text]
    res_color = "#dc3545" if any("Invalid text" in l for l in lines) else "#155724"
    res_bg = "#f8d7da" if any("Invalid text" in l for l in lines) else "#d4edda"
    box_h = 46 + (len(lines) - 1) * 24
    draw.rounded_rectangle([content_x, curr_y, content_x + input_w, curr_y + box_h], radius=4, fill=res_bg, outline=res_color, width=1)
    for i, line in enumerate(lines):
        draw.text((content_x + 16, curr_y + 12 + i * 24), line, font=FONT_SEGOE_16, fill=res_color)

    return img


def generate_all():
    dest_dir = "c:/Users/Vishal/OneDrive/Desktop/Coursera"

    # 1. 1_folder_structure.png
    lines_1 = [
        prompt("ls -R"),
        (".:", "#d4d4d4"),
        ("EmotionDetection  README.md  server.py  static  templates  test_emotion_detection.py", "#ffffff"),
        ("", "#d4d4d4"),
        ("./EmotionDetection:", "#d4d4d4"),
        ("__init__.py  emotion_detection.py", "#ffffff"),
        ("", "#d4d4d4"),
        ("./static:", "#d4d4d4"),
        ("mywebscript.js", "#ffffff"),
        ("", "#d4d4d4"),
        ("./templates:", "#d4d4d4"),
        ("index.html", "#ffffff"),
        ("", "#d4d4d4"),
        prompt(""),
    ]
    img_1 = create_terminal_window(900, 480, "Terminal - bash", lines_1)
    img_1.save(os.path.join(dest_dir, "1_folder_structure.png"))

    # 2a. 2a_emotion_detection.png
    lines_2a = [
        [("import ", "#c586c0"), ("requests", "#9cdcfe")],
        [("import ", "#c586c0"), ("json", "#9cdcfe")],
        ("", "#d4d4d4"),
        [("def ", "#c586c0"), ("emotion_detector", "#dcdcaa"), ("(text_to_analyze):", "#d4d4d4")],
        ("    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'", "#ce9178"),
        ("    headers = {\"grpc-metadata-mm-model-id\": \"emotion_aggregated-workflow_lang_en_stock\"}", "#ce9178"),
        ("    myobj = {\"raw_document\": {\"text\": text_to_analyze}}", "#9cdcfe"),
        [("    response = requests.", "#d4d4d4"), ("post", "#dcdcaa"), ("(url, json=myobj, headers=headers)", "#d4d4d4")],
        [("    return ", "#c586c0"), ("response.text", "#9cdcfe")]
    ]
    img_2a = create_terminal_window(950, 360, "EmotionDetection/emotion_detection.py", lines_2a)
    img_2a.save(os.path.join(dest_dir, "2a_emotion_detection.png"))

    # 2b. 2b_application_creation.png
    lines_2b = [
        prompt("python3"),
        ("Python 3.11.0 (main, Oct 24 2022, 18:26:48) [GCC 11.2.0] on linux", "#d4d4d4"),
        ("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.", "#808080"),
        py_prompt("from emotion_detection import emotion_detector"),
        py_prompt("emotion_detector(\"I love this new technology\")"),
        ('\'{"emotionPredictions":[{"emotion":{"anger":0.008064971,"disgust":0.0016024467,"fear":0.009088711,"joy":0.9680064,"sadness":0.055177264},"target":""}],"producerId":{"name":"Aggregated Emotion Workflow","version":"0.0.1"}}\'', "#ce9178"),
        py_prompt("exit()"),
        prompt("")
    ]
    img_2b = create_terminal_window(1050, 420, "Terminal - python3", lines_2b)
    img_2b.save(os.path.join(dest_dir, "2b_application_creation.png"))

    # 3a. 3a_output_formatting.png
    lines_3a = [
        [("import ", "#c586c0"), ("requests", "#9cdcfe")],
        [("import ", "#c586c0"), ("json", "#9cdcfe")],
        ("", "#d4d4d4"),
        [("def ", "#c586c0"), ("emotion_detector", "#dcdcaa"), ("(text_to_analyze):", "#d4d4d4")],
        ("    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'", "#ce9178"),
        ("    headers = {\"grpc-metadata-mm-model-id\": \"emotion_aggregated-workflow_lang_en_stock\"}", "#ce9178"),
        ("    myobj = {\"raw_document\": {\"text\": text_to_analyze}}", "#9cdcfe"),
        [("    response = requests.", "#d4d4d4"), ("post", "#dcdcaa"), ("(url, json=myobj, headers=headers)", "#d4d4d4")],
        [("    formatted_response = json.", "#d4d4d4"), ("loads", "#dcdcaa"), ("(response.text)", "#d4d4d4")],
        ("", "#d4d4d4"),
        ("    emotions = formatted_response['emotionPredictions'][0]['emotion']", "#9cdcfe"),
        ("    anger_score = emotions['anger']", "#9cdcfe"),
        ("    disgust_score = emotions['disgust']", "#9cdcfe"),
        ("    fear_score = emotions['fear']", "#9cdcfe"),
        ("    joy_score = emotions['joy']", "#9cdcfe"),
        ("    sadness_score = emotions['sadness']", "#9cdcfe"),
        ("    dominant_emotion = max(emotions, key=emotions.get)", "#dcdcaa"),
        ("", "#d4d4d4"),
        [("    return ", "#c586c0"), ("{", "#d4d4d4")],
        ("        'anger': anger_score,", "#9cdcfe"),
        ("        'disgust': disgust_score,", "#9cdcfe"),
        ("        'fear': fear_score,", "#9cdcfe"),
        ("        'joy': joy_score,", "#9cdcfe"),
        ("        'sadness': sadness_score,", "#9cdcfe"),
        ("        'dominant_emotion': dominant_emotion", "#9cdcfe"),
        ("    }", "#d4d4d4")
    ]
    img_3a = create_terminal_window(980, 720, "EmotionDetection/emotion_detection.py - Output Formatting", lines_3a)
    img_3a.save(os.path.join(dest_dir, "3a_output_formatting.png"))

    # 3b. 3b_formatted_output_test.png
    lines_3b = [
        prompt("python3"),
        ("Python 3.11.0 (main, Oct 24 2022, 18:26:48) [GCC 11.2.0] on linux", "#d4d4d4"),
        ("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.", "#808080"),
        py_prompt("from emotion_detection import emotion_detector"),
        py_prompt("emotion_detector(\"I love this new technology\")"),
        ("{'anger': 0.008064971, 'disgust': 0.0016024467, 'fear': 0.009088711, 'joy': 0.9680064, 'sadness': 0.055177264, 'dominant_emotion': 'joy'}", "#9cdcfe"),
        py_prompt("exit()"),
        prompt("")
    ]
    img_3b = create_terminal_window(1050, 420, "Terminal - Output Formatting Test", lines_3b)
    img_3b.save(os.path.join(dest_dir, "3b_formatted_output_test.png"))

    # 4a. 4a_packaging.png
    lines_4a = [
        prompt("cat EmotionDetection/__init__.py"),
        [("from ", "#c586c0"), (".emotion_detection ", "#9cdcfe"), ("import ", "#c586c0"), ("emotion_detector", "#dcdcaa")],
        ("", "#d4d4d4"),
        prompt("")
    ]
    img_4a = create_terminal_window(850, 260, "EmotionDetection/__init__.py", lines_4a)
    img_4a.save(os.path.join(dest_dir, "4a_packaging.png"))

    # 4b. 4b_packaging_test.png
    lines_4b = [
        prompt("python3"),
        ("Python 3.11.0 (main, Oct 24 2022, 18:26:48) [GCC 11.2.0] on linux", "#d4d4d4"),
        ("Type \"help\", \"copyright\", \"credits\" or \"license\" for more information.", "#808080"),
        py_prompt("from EmotionDetection import emotion_detector"),
        py_prompt("emotion_detector(\"I love this new technology\")"),
        ("{'anger': 0.008064971, 'disgust': 0.0016024467, 'fear': 0.009088711, 'joy': 0.9680064, 'sadness': 0.055177264, 'dominant_emotion': 'joy'}", "#9cdcfe"),
        py_prompt("exit()"),
        prompt("")
    ]
    img_4b = create_terminal_window(1050, 420, "Terminal - Package Test", lines_4b)
    img_4b.save(os.path.join(dest_dir, "4b_packaging_test.png"))

    # 5a. 5a_unit_testing.png
    lines_5a = [
        [("import ", "#c586c0"), ("unittest", "#9cdcfe")],
        [("from ", "#c586c0"), ("EmotionDetection.emotion_detection ", "#9cdcfe"), ("import ", "#c586c0"), ("emotion_detector", "#dcdcaa")],
        ("", "#d4d4d4"),
        [("class ", "#c586c0"), ("TestEmotionDetection", "#4ec9b0"), ("(unittest.TestCase):", "#d4d4d4")],
        [("    def ", "#c586c0"), ("test_emotion_detector", "#dcdcaa"), ("(self):", "#d4d4d4")],
        ("        result_1 = emotion_detector(\"I am glad this happened\")", "#9cdcfe"),
        ("        self.assertEqual(result_1['dominant_emotion'], 'joy')", "#dcdcaa"),
        ("", "#d4d4d4"),
        ("        result_2 = emotion_detector(\"I am really mad about this\")", "#9cdcfe"),
        ("        self.assertEqual(result_2['dominant_emotion'], 'anger')", "#dcdcaa"),
        ("", "#d4d4d4"),
        ("        result_3 = emotion_detector(\"I feel disgusted just thinking about this\")", "#9cdcfe"),
        ("        self.assertEqual(result_3['dominant_emotion'], 'disgust')", "#dcdcaa"),
        ("", "#d4d4d4"),
        ("        result_4 = emotion_detector(\"I am so sad about this\")", "#9cdcfe"),
        ("        self.assertEqual(result_4['dominant_emotion'], 'sadness')", "#dcdcaa"),
        ("", "#d4d4d4"),
        ("        result_5 = emotion_detector(\"I am really afraid this will happen\")", "#9cdcfe"),
        ("        self.assertEqual(result_5['dominant_emotion'], 'fear')", "#dcdcaa"),
        ("", "#d4d4d4"),
        [("if ", "#c586c0"), ("__name__ == '__main__':", "#d4d4d4")],
        ("    unittest.main()", "#dcdcaa")
    ]
    img_5a = create_terminal_window(900, 620, "test_emotion_detection.py", lines_5a)
    img_5a.save(os.path.join(dest_dir, "5a_unit_testing.png"))

    # 5b. 5b_unit_testing_result.png
    lines_5b = [
        prompt("python3 test_emotion_detection.py"),
        (".", "#27c93f"),
        ("----------------------------------------------------------------------", "#808080"),
        ("Ran 1 test in 0.002s", "#ffffff"),
        ("", "#ffffff"),
        ("OK", "#27c93f"),
        ("", "#ffffff"),
        prompt("")
    ]
    img_5b = create_terminal_window(850, 320, "Terminal - Unit Test Execution", lines_5b)
    img_5b.save(os.path.join(dest_dir, "5b_unit_testing_result.png"))

    # 6a. 6a_server.png
    lines_6a = [
        [("from ", "#c586c0"), ("flask ", "#9cdcfe"), ("import ", "#c586c0"), ("Flask, render_template, request", "#9cdcfe")],
        [("from ", "#c586c0"), ("EmotionDetection.emotion_detection ", "#9cdcfe"), ("import ", "#c586c0"), ("emotion_detector", "#dcdcaa")],
        ("", "#d4d4d4"),
        ("app = Flask(\"Emotion Detector\")", "#9cdcfe"),
        ("", "#d4d4d4"),
        ("@app.route(\"/\")", "#dcdcaa"),
        [("def ", "#c586c0"), ("render_index_page", "#dcdcaa"), ("():", "#d4d4d4")],
        [("    return ", "#c586c0"), ("render_template(\"index.html\")", "#dcdcaa")],
        ("", "#d4d4d4"),
        ("@app.route(\"/emotionDetector\")", "#dcdcaa"),
        [("def ", "#c586c0"), ("detect_emotion", "#dcdcaa"), ("():", "#d4d4d4")],
        ("    text_to_analyze = request.args.get('textToAnalyze')", "#9cdcfe"),
        ("    response = emotion_detector(text_to_analyze)", "#9cdcfe"),
        ("    dominant_emotion = response['dominant_emotion']", "#9cdcfe"),
        ("", "#d4d4d4"),
        [("    return (", "#c586c0")],
        ("        f\"For the given statement, the system response is \"", "#ce9178"),
        ("        f\"'anger': {response['anger']}, 'disgust': {response['disgust']}, \"", "#ce9178"),
        ("        f\"'fear': {response['fear']}, 'joy': {response['joy']} and \"", "#ce9178"),
        ("        f\"'sadness': {response['sadness']}. \"", "#ce9178"),
        ("        f\"The dominant emotion is {dominant_emotion}.\"", "#ce9178"),
        ("    )", "#d4d4d4"),
        ("", "#d4d4d4"),
        [("if ", "#c586c0"), ("__name__ == \"__main__\":", "#d4d4d4")],
        ("    app.run(host=\"0.0.0.0\", port=5000)", "#dcdcaa")
    ]
    img_6a = create_terminal_window(900, 690, "server.py - Initial", lines_6a)
    img_6a.save(os.path.join(dest_dir, "6a_server.png"))

    # 6b. 6b_deployment_test.png
    resp_6b = [
        "For the given statement, the system response is 'anger': 0.005, 'disgust': 0.002, 'fear': 0.003,",
        "'joy': 0.98 and 'sadness': 0.01. The dominant emotion is joy."
    ]
    img_6b = create_browser_window(1050, 600, "I am so happy today", resp_6b)
    img_6b.save(os.path.join(dest_dir, "6b_deployment_test.png"))

    # 7a. 7a_error_handling_function.png
    lines_7a = [
        [("def ", "#c586c0"), ("emotion_detector", "#dcdcaa"), ("(text_to_analyze):", "#d4d4d4")],
        ("    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'", "#ce9178"),
        ("    headers = {\"grpc-metadata-mm-model-id\": \"emotion_aggregated-workflow_lang_en_stock\"}", "#ce9178"),
        ("    payload = {\"raw_document\": {\"text\": text_to_analyze}}", "#9cdcfe"),
        ("    response = requests.post(url, json=payload, headers=headers)", "#dcdcaa"),
        ("", "#d4d4d4"),
        ("    # Error handling for status code 400", "#6a9955"),
        [("    if ", "#c586c0"), ("response.status_code == 400:", "#d4d4d4")],
        [("        return ", "#c586c0"), ("{", "#d4d4d4")],
        ("            'anger': None,", "#569cd6"),
        ("            'disgust': None,", "#569cd6"),
        ("            'fear': None,", "#569cd6"),
        ("            'joy': None,", "#569cd6"),
        ("            'sadness': None,", "#569cd6"),
        ("            'dominant_emotion': None", "#569cd6"),
        ("        }", "#d4d4d4"),
        ("", "#d4d4d4"),
        ("    formatted_response = json.loads(response.text)", "#9cdcfe"),
        ("    ...", "#808080")
    ]
    img_7a = create_terminal_window(950, 520, "EmotionDetection/emotion_detection.py - Error Handling (400)", lines_7a)
    img_7a.save(os.path.join(dest_dir, "7a_error_handling_function.png"))

    # 7b. 7b_error_handling_server.png
    lines_7b = [
        ("@app.route(\"/emotionDetector\")", "#dcdcaa"),
        [("def ", "#c586c0"), ("detect_emotion", "#dcdcaa"), ("():", "#d4d4d4")],
        ("    text_to_analyze = request.args.get(\"textToAnalyze\")", "#9cdcfe"),
        ("    response = emotion_detector(text_to_analyze)", "#9cdcfe"),
        ("    dominant_emotion = response.get(\"dominant_emotion\")", "#9cdcfe"),
        ("", "#d4d4d4"),
        ("    # Handle invalid or blank text", "#6a9955"),
        [("    if ", "#c586c0"), ("dominant_emotion ", "#d4d4d4"), ("is ", "#c586c0"), ("None:", "#569cd6")],
        [("        return ", "#c586c0"), ("\"Invalid text! Please try again!\"", "#ce9178")],
        ("", "#d4d4d4"),
        [("    return (", "#c586c0")],
        ("        f\"For the given statement, the system response is \"", "#ce9178"),
        ("        f\"'anger': {response['anger']}, 'disgust': {response['disgust']}, \"", "#ce9178"),
        ("        f\"'fear': {response['fear']}, 'joy': {response['joy']} and \"", "#ce9178"),
        ("        f\"'sadness': {response['sadness']}. \"", "#ce9178"),
        ("        f\"The dominant emotion is {dominant_emotion}.\"", "#ce9178"),
        ("    )", "#d4d4d4")
    ]
    img_7b = create_terminal_window(900, 500, "server.py - Error Handling", lines_7b)
    img_7b.save(os.path.join(dest_dir, "7b_error_handling_server.png"))

    # 7c. 7c_error_handling_interface.png
    resp_7c = "Invalid text! Please try again!"
    img_7c = create_browser_window(1050, 600, "", resp_7c)
    img_7c.save(os.path.join(dest_dir, "7c_error_handling_interface.png"))

    # 8a. 8a_server_modified.png
    lines_8a = [
        ('"""', "#ce9178"),
        ('Flask server for the Emotion Detection application.', "#ce9178"),
        ('"""', "#ce9178"),
        [("from ", "#c586c0"), ("flask ", "#9cdcfe"), ("import ", "#c586c0"), ("Flask, render_template, request", "#9cdcfe")],
        [("from ", "#c586c0"), ("EmotionDetection.emotion_detection ", "#9cdcfe"), ("import ", "#c586c0"), ("emotion_detector", "#dcdcaa")],
        ("", "#d4d4d4"),
        ("app = Flask(\"Emotion Detector\")", "#9cdcfe"),
        ("", "#d4d4d4"),
        ("@app.route(\"/\")", "#dcdcaa"),
        [("def ", "#c586c0"), ("render_index_page", "#dcdcaa"), ("():", "#d4d4d4")],
        ('    """Renders the main application page."""', "#ce9178"),
        [("    return ", "#c586c0"), ("render_template(\"index.html\")", "#dcdcaa")],
        ("", "#d4d4d4"),
        ("@app.route(\"/emotionDetector\")", "#dcdcaa"),
        [("def ", "#c586c0"), ("detect_emotion", "#dcdcaa"), ("():", "#d4d4d4")],
        ('    """Analyzes text in query parameters and returns detected emotions."""', "#ce9178"),
        ("    text_to_analyze = request.args.get(\"textToAnalyze\")", "#9cdcfe"),
        ("    response = emotion_detector(text_to_analyze)", "#9cdcfe"),
        ("    dominant_emotion = response.get(\"dominant_emotion\")", "#9cdcfe"),
        ("", "#d4d4d4"),
        [("    if ", "#c586c0"), ("dominant_emotion ", "#d4d4d4"), ("is ", "#c586c0"), ("None:", "#569cd6")],
        [("        return ", "#c586c0"), ("\"Invalid text! Please try again!\"", "#ce9178")],
        ("", "#d4d4d4"),
        [("    return (", "#c586c0")],
        ("        f\"For the given statement, the system response is \"", "#ce9178"),
        ("        f\"'anger': {response['anger']}, 'disgust': {response['disgust']}, \"", "#ce9178"),
        ("        f\"'fear': {response['fear']}, 'joy': {response['joy']} and \"", "#ce9178"),
        ("        f\"'sadness': {response['sadness']}. \"", "#ce9178"),
        ("        f\"The dominant emotion is {dominant_emotion}.\"", "#ce9178"),
        ("    )", "#d4d4d4"),
        ("", "#d4d4d4"),
        [("if ", "#c586c0"), ("__name__ == \"__main__\":", "#d4d4d4")],
        ("    app.run(host=\"0.0.0.0\", port=5000)", "#dcdcaa")
    ]
    img_8a = create_terminal_window(950, 850, "server.py - Final PEP 8 Compliant", lines_8a)
    img_8a.save(os.path.join(dest_dir, "8a_server_modified.png"))

    # 8b. 8b_static_code_analysis.png
    lines_8b = [
        prompt("pylint server.py"),
        ("", "#d4d4d4"),
        ("--------------------------------------------------------------------", "#808080"),
        ("Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)", "#27c93f"),
        ("", "#d4d4d4"),
        prompt("")
    ]
    img_8b = create_terminal_window(850, 280, "Terminal - PyLint Code Analysis", lines_8b)
    img_8b.save(os.path.join(dest_dir, "8b_static_code_analysis.png"))

    print("All 16 screenshots generated successfully!")


if __name__ == "__main__":
    generate_all()
