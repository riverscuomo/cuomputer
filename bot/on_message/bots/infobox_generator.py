import requests
import re
import io
from discord import File
from PIL import Image, ImageDraw, ImageFont


class InfoboxGenerator:

    supported_types = ['Album']

    album_types = {
        'studio': ('Studio album by', (170, 190, 215)),
        'recording session': ('Recording session by', (143, 188, 143)),
        'demo': ('Demo album by', (143, 188, 143)),
        'ep': ('EP by', (143, 188, 143)),
        'live': ('Live album by', (222, 184, 135)),
        'greatest': ('Greatest hits by', (143, 188, 143)),
        'remix': ('Remix album by', (143, 188, 143)),
        'box': ('Box set by', (143, 188, 143)),
        'compilation': ('Compilation album by', (143, 188, 143)),
        'cover': ('Cover version by', (216, 191, 216)),
        'tribute': ('Tribute album by', (216, 191, 216)),
        'soundtrack': ('Soundtrack by', (220, 220, 220)),
        'televison': ('Soundtrack by', (220, 220, 220)),
        'film': ('Film score by', (220, 220, 220)),
        'video': ('Music video by', (153, 204, 255)),
        'unofficial bootleg': ('Unofficial bootleg by', (255, 180, 249)),
        'digital compilation': ('Digital compilation by', (143, 188, 143)),
    }

    fonts = {
        'small': ImageFont.truetype('data/fonts/Roboto-Regular.ttf', 25),
        'reg': ImageFont.truetype('data/fonts/Roboto-Regular.ttf', 32),
        'medium-bold': ImageFont.truetype('data/fonts/Roboto-Bold.ttf', 28),
        'bold': ImageFont.truetype('data/fonts/Roboto-Bold.ttf', 32),
        'title': ImageFont.truetype('data/fonts/Roboto-Bold.ttf', 50),
    }

    def __init__(self, full_content, weezerpedia_api):
        infobox_data, infobox_type = self.extract_template_data(
            full_content, 'Infobox')

        self.infobox_data = infobox_data
        self.infobox_type = infobox_type
        self.weezerpedia_api = weezerpedia_api
        self.tracklist = self.extract_template_data(
            full_content, 'Track listing')[0]

    def generate_infobox(self):

        if self.infobox_data is None or self.infobox_type not in self.supported_types:
            return None

        # Create a blank image with white background
        image = Image.new('RGB', (1200, 600), color='white')
        draw = ImageDraw.Draw(image)

        match self.infobox_type:
            case 'Album':
                # Draw thumbnail
                cover_img_url = self.weezerpedia_api.get_file_url(
                    self.infobox_data['Cover'])
                self.draw_thumbnail(image, draw, cover_img_url)

                release_date = self.infobox_data.get(
                    'Released', 'Unknown date')
                year_re = re.search(r'\d{4}', release_date)
                if year_re:
                    release_date = release_date[:year_re.end()]

                # Draw essential panel
                self.draw_essential_panel(draw, self.infobox_data.get(
                    'Name', 'Untitled') or 'Untitled', release_date or 'Unknown release date')

                # Draw main panel
                album_type, color = self.album_types.get(self.infobox_data.get(
                    'Type', 'studio').lower(), ('Studio album by', (170, 190, 215)))
                self.draw_main_panel(draw, album_type, self.infobox_data.get(
                    'Artist', 'Unknown') or 'Unknown', color)

                margin = 45
                line_count = 0
                line_count += self.draw_feature_text(draw, 'Length:', self.infobox_data.get(
                    'Length', 'Unknown').replace('<br>', ' - '), 'Unknown', 95)
                line_count += self.draw_feature_text(draw, 'Label:', self.infobox_data.get(
                    'Label', 'Unknown').replace('<br>', ', '), 'No label', 95 + margin * line_count)
                line_count += self.draw_feature_text(draw, 'Genre:', self.infobox_data.get(
                    'Genre', 'Unknown').replace('<br>', ', '), 'Unkown', 95 + margin * line_count)
                line_count += self.draw_feature_text(draw, 'Producers:', self.infobox_data.get(
                    'Producer', 'No producer').replace('<br>', ', '), 'No producers', 95 + margin * line_count)

                # Track listing
                draw.text((430, 95 + margin * line_count + 30),
                          'Track listing', fill=color, font=self.fonts['bold'])
                if self.tracklist:
                    self.draw_tracklist(
                        draw, 95 + margin * line_count + 80, color)
                else:
                    draw.text((430, 95 + margin * line_count + 80), 'No tracklist available',
                              fill=(184, 185, 186), font=self.fonts['reg'])

        with io.BytesIO() as image_binary:
            image.save(image_binary, 'JPEG')
            image_binary.seek(0)
            return File(image_binary, filename=f"infobox_{self.infobox_type}.jpg")

    def draw_thumbnail(self, image, draw, thumbnail_url):
        if thumbnail_url is None:
            draw.rectangle([0, 0, 400, 400], fill='#1c1e20')
            draw.text((200, 200), 'No cover', fill='white',
                      font=self.fonts['bold'], anchor='mm')
            return

        # Load the cover image
        cover_img = Image.open(requests.get(thumbnail_url, stream=True).raw)
        cover_img.thumbnail((400, 400))
        cover_img = cover_img.resize((400, 400))

        # Paste the cover image on the main image
        image.paste(cover_img, (0, 0))

    # Draw the essential panel right below the thumbnail

    def draw_essential_panel(self, draw, title, subtitle):
        # Draw main info below the cover image
        draw.rectangle([0, 400, 400, 600], fill='#23272a')
        name, line_count = self.get_wrapped_text(
            title, self.fonts['title'], 400 - 22)
        draw.multiline_text((22, 410), name or 'Unknown',
                            fill='white', font=self.fonts['title'])

        # Subtitle
        draw.text((22, 410 + (line_count * 50) + 10), subtitle,
                  fill=(184, 185, 186), font=self.fonts['small'])

    # Draw the main panel on the right side of the image

    def draw_main_panel(self, draw, text, bold_text, color):
        # Draw main info panel
        draw.rectangle([400, 0, 1200, 600], fill='#2c2f33')

        # Draw header
        draw.rectangle([400, 0, 1200, 70], fill=color)
        initial_width = draw.textlength(text + ' ', font=self.fonts['reg'])
        draw.text((420, 33-(32/2)), text,
                  fill='#23272a', font=self.fonts['reg'])
        draw.text((420+initial_width, 33-(32/2)), bold_text,
                  fill='#23272a', font=self.fonts['bold'])

    # Draw infobox feature (e.g. 'Artist: Weezer') on the main panel. Returns the number of lines drawn

    def draw_feature_text(self, draw, label, value, no_value_text, y):
        # Draw label
        if value.strip() == '':
            value = no_value_text
        draw.text((430, y), label, fill='#d4d5d6', font=self.fonts['reg'])
        label_width = draw.textlength(label + ' ', font=self.fonts['reg'])

        # Draw value
        value = re.sub(r"<.*?>", "", value)
        parsed_value, line_count = self.get_wrapped_text(
            value, self.fonts['bold'], 1200 - 430 - label_width - 20, 2)
        draw.multiline_text((430 + label_width, y), parsed_value,
                            fill='#eaeaeb', font=self.fonts['bold'], spacing=15)

        return line_count

    # Draw the tracklist on the main panel
    def draw_tracklist(self, draw, y, color):
        track_count = 0
        for i in range(1, 20):
            track_name = self.tracklist.get(f'title{i}', None)
            if track_name:
                track_count += 1
            else:
                break

        items_per_column = (600 - y) // 43

        for i in range(1, track_count + 1):
            column_x = 430 if i <= items_per_column else 765 + 50
            item_y = y + ((i - 1) % items_per_column) * 43

            # If new column, re-draw the background to avoid overlapping
            if i % items_per_column == 1:
                draw.rectangle([column_x - 30, y, 1200, 600], fill='#2c2f33')

            if i == 2 * items_per_column and track_count != i:
                draw.text(
                    (column_x, item_y), f'.. and {track_count - i + 1} more tracks', fill=color, font=self.fonts['medium-bold'])
                break

            # Draw track number
            track_nb = str(i) + '.'
            draw.text((column_x, item_y), track_nb, fill=color,
                      font=self.fonts['medium-bold'])
            nb_text_width = draw.textlength(
                track_nb + ' ', font=self.fonts['medium-bold'])

            # Draw track name
            track_name = self.tracklist[f'title{i}']
            draw.text((column_x + nb_text_width, item_y), track_name,
                      fill='#ffffff', font=self.fonts['medium-bold'])

    # Extract data from a template (e.g. {{Infobox ...}}) and return it as a dictionary
    def extract_template_data(self, full_content, template_name):

        # Get template position in the content
        template_start = full_content.find('{{' + template_name)
        if template_start == -1:
            return None, None

        template_data = {}
        template_type = None  # {{Infobox Album ...}} would be 'Album'
        nested_level = 0  # Track nested template levels
        level_names_stack = []  # Stack to keep track of nested template names

        for line in full_content[template_start:].split('\n'):
            line = line.strip()
            if line.startswith('|'):
                # Extract key-value pairs from the template
                if nested_level > 0:
                    key, value = line[1:].split('=', 1)
                    current_dict = template_data
                    # Add the key-value pair to the dictionary at the appropriate nested level
                    for level_name in level_names_stack:
                        if level_name not in current_dict:
                            current_dict[level_name] = {}
                        current_dict = current_dict[level_name]
                    current_dict[key.strip()] = value.strip()
            if line.startswith('{{' + template_name):
                nested_level += 1
                template_type = line[2:].split()[1]
            elif line.startswith('{{'):
                nested_level += 1
                level_names_stack.append(line[2:].split()[0])
            elif line.startswith('}}'):
                nested_level -= 1
                if nested_level == 0:
                    break
                else:
                    level_names_stack.pop()

        return template_data, template_type

    # Wrap text to fit within a certain width. Returns the wrapped text and the number of lines

    def get_wrapped_text(self, text: str, font: ImageFont.ImageFont, line_length: int, max_lines: int = 10):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                if len(lines) == max_lines:
                    lines[-1] = lines[-1][:len(lines[-1])-3] + '...'
                    break
                lines.append(word)
        return '\n'.join(lines), len(lines)
