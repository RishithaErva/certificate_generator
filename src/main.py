import os
import json
import csv
import zipfile
from dotenv import load_dotenv
from logger import get_logger
from emailUtils import send_email_with_attachment
from scikitUtil import generate_certificate

# Load environment variables from .env file
load_dotenv()

logger = get_logger(__name__)

def main():
    print("1. Generate single certificate")
    print("2. Generate bulk certificates")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        try:
            generate_single_certificate()
        except Exception as e:
            logger.error(f"Error occurred while generating single certificate: {e}")
    elif choice == '2':
        try:
            generate_bulk_certificates()
        except Exception as e:
            logger.error(f"Error occurred while generating bulk certificates: {e}")
    else:
        logger.warning("Invalid choice entered. Please enter 1 or 2.")

def get_font_params():
    return {
        "font_size": {
            "heading": 27,
            "certificate_about": 12,
            "certificant_name": 25,
            "date": 12,
            "company_name": 12,
            "certificate_provider_name": 12
        },
        "font_family": {
            "heading": "Times New Roman",
            "certificate_about": "Georgia",
            "certificant_name": "Verdana",
            "date": "Book Antiqua",
            "company_name": "Verdana",
            "certificate_provider_name": "Book Antiqua"
        },
        "font_color": {
            "heading": "black",
            "certificate_about": "black",
            "certificant_name": "navy",
            "date": "black",
            "company_name": "black",
            "certificate_provider_name": "black"
        },
        "position": {
            "heading": [930, 325],
            "certificate_about": [950, 640],
            "certificant_name": [970, 625],
            "date": [450, 1070],
            "company_name": [10, 140],
            "certificate_provider_name": [1275, 1070]
        }
    }

def load_and_substitute_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    for key, value in config.items():
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            config[key] = os.getenv(env_var, value)
    return config

def generate_single_certificate():
    single_cert_data = load_and_substitute_config('config/singlecert.json')

    logger.debug("Entering generate_single_certificate function...")

    template_image_path = single_cert_data["template_image_path"]
    heading = single_cert_data["heading"]
    certificate_about = single_cert_data["certificate_about"]
    certificant_name = single_cert_data["certificant_name"]
    date = single_cert_data["date"]
    company_name = single_cert_data["company_name"]
    certificate_provider_name = single_cert_data["certificate_provider_name"]
    
    font_params = get_font_params()
    font_size = font_params["font_size"]
    font_family = font_params["font_family"]
    font_color = font_params["font_color"]
    position = font_params["position"]

    try:
        generate_certificate(template_image_path, heading, certificate_about, certificant_name, date, company_name, certificate_provider_name, font_size, font_family, font_color, position)
        logger.info("Single certificate generated successfully.")

    except Exception as e:
        logger.error(f"Error occurred while generating single certificate: {e}")

    finally:
        logger.debug("Exiting generate_single_certificate function...")

def generate_bulk_certificates():
    bulk_cert_data = load_and_substitute_config('config/bulkcert.json')

    template_image_path = bulk_cert_data["template_image_path"]
    heading = bulk_cert_data["heading"]
    certificate_about = bulk_cert_data["certificate_about"]
    csv_file_path = bulk_cert_data["csv_file_path"]
    date = bulk_cert_data["date"]
    company_name = bulk_cert_data["company_name"]
    certificate_provider_name = bulk_cert_data["certificate_provider_name"]
    num_certificates = bulk_cert_data["num_certificates"]
    recipient_email = bulk_cert_data["email_address"]

    sender_email = os.getenv('SENDER_EMAIL')
    app_password = os.getenv('APP_PASSWORD')
    
    font_params = get_font_params()
    font_size = font_params["font_size"]
    font_family = font_params["font_family"]
    font_color = font_params["font_color"]
    position = font_params["position"]
    
    logger.debug("Entering generate_bulk_certificates function...")

    zip_file_path = os.path.join(os.getenv('OUTPUT_DIR'), 'certificates.zip')
    try:
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                certificates_generated = 0 
                for row in reader:
                    if certificates_generated >= num_certificates:
                        break
                    certificant_name = row[0]

                    generate_certificate(template_image_path, heading, certificate_about, certificant_name, date, company_name, certificate_provider_name, font_size, font_family, font_color, position)
                    
                    cert_path = os.path.join(os.getenv('OUTPUT_DIR'), f'{certificant_name}.png')
                    zipf.write(cert_path, os.path.basename(cert_path))

                    certificates_generated += 1
        logger.info(f"{num_certificates} bulk certificates generated successfully.")

        subject = "Certificates"
        body = "Please find the attached certificates."
        send_email_with_attachment(sender_email, app_password, recipient_email, subject, body, zip_file_path)

    except Exception as e:
        logger.error(f"Error occurred while generating bulk certificates: {e}")

    finally:
        logger.debug("Exiting generate_bulk_certificates function...")

if __name__ == "__main__":
    main()
