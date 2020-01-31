import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def main():
    parser = argparse.ArgumentParser(description='Chcesz wiedzieć czy jest lepsza cena Twojej wycieczki?')
    parser.add_argument('-n', type=str, help='Kod pokoju')
    parser.add_argument('-p', type=int, help='Cena')

    args = parser.parse_args()
    my_price = args.p
    my_room_code = args.n
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    browser.get(
        'https://www.tui.pl/wypoczynek/grecja/zakynthos/tui-suneo-cavo-doro-zth15115/OfferCodeWS'
        '/WAWZTH20200515145520200515202005221915L07ZTH15115DZX3AA02')

    delay = 3  # seconds
    my_room_exist = False
    try:
        my_elem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH,
                                                                                      '/html/body/div[1]/div[2]'
                                                                                      '/main/div[2]/div/div/div[3]'
                                                                                      '/div/div/div/div/div[2]/div[2]'
                                                                                      '/table/tbody')))
        rooms = my_elem.find_elements_by_xpath("./tr[*]")
        for room in rooms:
            room_code = room.find_element_by_xpath('./td[*]/ul/li[1]/span[2]')
            if my_room_code.lower() in room_code.text.lower():
                print(room_code.text)
                try:
                    room_price = room.find_element_by_xpath('./td[5]/div/div/div/div/span')
                except:
                    room_price = room.find_element_by_xpath('./td[4]/div/div/div/div/span')
                cena = "".join(room_price.text.split())
                print(cena)
                if int(cena) < my_price:
                    print('lepsza cena!')
                else:
                    print('dupa, czekamy dalej')
                print('-------------------')
                my_room_exist = True
                break
        if not my_room_exist:
            print("nie ma oferty dla pokoju " + my_room_code)
    except TimeoutException:
        print("Loading took too much time!")

    browser.quit()


if __name__ == "__main__":
    main()
