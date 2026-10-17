from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pathlib import Path

import click


MONTHS = {
    "Janvier": 1,
    "Février": 2,
    "Mars": 3,
    "Avril": 4,
    "Mai": 5,
    "Juin": 6,
    "Juillet": 7,
    "Août": 8,
    "Septembre": 9,
    "Octobre": 10,
    "Novembre": 11,
    "Décembre": 12,
}

ELEMENT_TIMEOUT = 5
DOCURL = "https://candidat.francetravail.fr/candidat/situationadministrative/uploaddocuments/selectiondocument"

driver = webdriver.Chrome()
driver.get(DOCURL)

title = driver.title


def cookies():
    try:
        cookies_root = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//pe-cookies"))
        )
        shadow = cookies_root.shadow_root
        cookies_button = WebDriverWait(shadow, ELEMENT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "pecookies-continue-btn"))
        )
        cookies_button.click()
    except TimeoutException:
        print("No shadow root")

    print("Cookies refused - any announcements?")

    try:
        know_button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='know_btn know_btn-strong']")
            )
        )
        know_button.click()
    except TimeoutException:
        print("No announcement button")


def login(user, password):
    print("Now log in")

    for field, value in [("identifiant", user), ("password", password)]:
        WebDriverWait(driver, ELEMENT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, field))
        ).send_keys(value)

    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "submit"))
    ).click()

    print(80 * "=")
    input("Do the 2-factor auth, then press enter to continue")


def upload(docs_path):
    print("Select context")
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "listeDeroulanteContexte"))
    ).click()
    WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, "//option[@value='7']"))
    ).click()

    upload_next_document(docs_path)


def upload_next_document(docs_path):
    label = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//td[@headers='col-03']/label[@for='radio']")
        )
    )
    validate_button = driver.find_element(by=By.ID, value="valider")

    label.click()
    print(label.text)

    wanted_document = label.text
    if wanted_document.startswith("Bulletin de salaire"):
        month = MONTHS[wanted_document.split(" ")[7]]
        year = wanted_document.split(" ")[8]
        document_path = docs_path / year / f"{month:02d}.{year}.pdf"
        print(f"Document {document_path.as_posix()} exists: {document_path.exists()}")
    else:
        document_path = Path("")

    validate_button.click()

    file_button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "filePourMultiple"))
    )
    file_button.send_keys(document_path.as_posix())
    validate_button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "valider"))
    )
    validate_button.click()
    print(80 * "=")
    input(f"Uploading ${document_path.as_posix()} - press enter to confirm")

    confirm_button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span/button[contains(text(), 'Confirmer')]")
        )
    )
    confirm_button.click()
    another_document_link = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//main/div/div/div/a[contains(text(), 'envoyer un autre document')]",
            )
        )
    )
    another_document_link.click()
    upload_next_document(docs_path)


@click.command
@click.option("--user", help="Username for FranceTravail")
@click.option("--password", help="Password for FranceTravail")
@click.option("--docs-path", help="Full path under which your pay slips can be found")
def cli(user, password, docs_path):
    cookies()
    login(user, password)
    upload(docs_path)


if __name__ == "__main__":
    cli()
