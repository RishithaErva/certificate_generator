import os
from skimage import io
import matplotlib.pyplot as plt
from logger import get_logger

logger = get_logger(__name__)

def generate_certificate(template_image_path, heading, certificate_about, certificant_name, date, company_name, certificate_provider_name,
                         font_size, font_family, font_color, position, output_dir=None):
    try:
        logger.info("Generating certificate...")
        
        # Load the template image
        template_image = io.imread(template_image_path)
        
        fig, ax = plt.subplots()
        ax.imshow(template_image)

        certificate_about = certificate_about.replace('[certificant_name]', certificant_name)

        parts = certificate_about.split(certificant_name, 1)
        if len(parts) > 1:
            first_line = parts[0]
            remaining_text = parts[1]
        else:
            first_line = certificate_about
            remaining_text = ""

        certificate_about = '\n\n'.join([first_line.strip(), " ", remaining_text.strip()])

        ax.text(position["heading"][0], position["heading"][1], heading, fontsize=font_size["heading"], fontfamily=font_family["heading"], color=font_color["heading"], ha='center', va='center', weight='bold')
        ax.text(position["certificate_about"][0], position["certificate_about"][1], certificate_about, fontsize=font_size["certificate_about"], fontfamily=font_family["certificate_about"], color=font_color["certificate_about"], ha='center', va='center')
        ax.text(position["certificant_name"][0], position["certificant_name"][1], certificant_name, fontsize=font_size["certificant_name"], fontfamily=font_family["certificant_name"], color=font_color["certificant_name"], ha='center', va='center', fontstyle='italic', weight='bold')
        ax.text(position["date"][0], position["date"][1], date, fontsize=font_size["date"], fontfamily=font_family["date"], color=font_color["date"], fontstyle='italic')
        ax.text(position["company_name"][0], position["company_name"][1], company_name, fontsize=font_size["company_name"], fontfamily=font_family["company_name"], color=font_color["company_name"])
        ax.text(position["certificate_provider_name"][0], position["certificate_provider_name"][1], certificate_provider_name, fontsize=font_size["certificate_provider_name"], fontfamily=font_family["certificate_provider_name"], color=font_color["certificate_provider_name"], fontstyle='italic')

        ax.axis('off')

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            certificate_output_path = os.path.join(output_dir, f'{certificant_name}.png')
        else:
            certificate_output_path = os.path.join('output', f'{certificant_name}.png')

        plt.savefig(certificate_output_path, dpi=300, bbox_inches='tight', pad_inches=0)

        plt.close()
        logger.info("Certificate generated successfully.")
    except Exception as e:
        logger.error(f"Error occurred while generating certificate: {e}")
