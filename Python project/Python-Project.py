import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your chromedriver executable
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'


def get_price_amazon(product_name):
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    driver.get(f'https://www.amazon.in/s?k={product_name}')
    time.sleep(3)  # Let the page load
    try:
        price_element = driver.find_element(By.CLASS_NAME, 'a-price-whole')
        price = price_element.text
    except:
        price = 'N/A'
    driver.quit()
    return price


def get_price_croma(product_name):
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    driver.get(f'https://www.croma.com/searchB?q={product_name}')
    time.sleep(5)  # Let the page load for 5 seconds
    try:
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'price-rating-wrap.plp-price-margin.plp-prices'))
        )
        price = price_element.text
    except Exception as e:
        print(f"Error fetching Croma price: {e}")
        price = 'N/A'
    finally:
        driver.quit()
    return price


def get_price_myntra(product_name):
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
    driver.get(f'https://www.myntra.com/t-shirt?rawQuery={product_name}')
    time.sleep(3)  # Let the page load
    try:
        # Wait until the first product is clickable and click it
        first_product = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//li[contains(@class, "product-base")][1]'))
        )
        first_product.click()
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[1])
        # Wait for the price element to be present on the product page
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pdp-price'))
        )
        price = price_element.text
    except Exception as e:
        print(f"Error fetching Myntra price: {e}")
        price = 'N/A'
    finally:
        driver.quit()
    return price


def convert_price(price_text):
    try:
        return float(price_text.replace(',', '').replace('₹', '').strip())
    except:
        return float('inf')


def search_prices():
    product_name = entry.get()
    if not product_name:
        messagebox.showwarning('Input Error', 'Please enter a product name.')
        return

    amazon_price = get_price_amazon(product_name)
    croma_price = get_price_croma(product_name)
    myntra_price = get_price_myntra(product_name)

    amazon_price_val = convert_price(amazon_price)
    croma_price_val = convert_price(croma_price)
    myntra_price_val = convert_price(myntra_price)

    prices = {
        'Amazon': amazon_price_val,
        'Croma': croma_price_val,
        'Myntra': myntra_price_val
    }

    # Determine the lowest price and corresponding source
    min_price_source = min(prices, key=lambda x: prices[x])
    min_price = prices[min_price_source]

    result_text = (
        f"Amazon: {amazon_price}\n"
        f"Croma: {croma_price}\n"
        f"Myntra: {myntra_price}\n\n"
        f"Lowest Price: {min_price_source} ₹{min_price}" if min_price != float(
            'inf') else "Prices not available"
    )
    result_label.config(text=result_text)


# GUI Setup
root = tk.Tk()
root.title("Product Price Scraper")

tk.Label(root, text="Enter Product Name:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)
tk.Button(root, text="Search Prices", command=search_prices).pack(pady=5)
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(pady=10)

root.mainloop()
