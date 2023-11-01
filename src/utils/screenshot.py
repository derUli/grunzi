
def make_screenshot(self, screen):
    screenshot_dir = os.path.join(get_userdata_path(), 'screenshots')

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_file = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )
