from selenium import webdriver

driver = webdriver.Firefox()

driver.get("http://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGHHE.03/2016/001/contents.html")
# driver.execute_script("var url = new String(document.forms[0].url.value);var url_parts = url.split(\"?\");if (url_parts[1] != null) {var ascii_url = url_parts[0] + \".ascii?\" + url_parts[1];}else {var ascii_url = url_parts[0] + \".ascii?\";}")


# loadMore =driver.find_elements_by_xpath("html/body/pre/table/tbody/tr")
loadMore =driver.find_elements_by_tag_name('a')
# loadMore = driver.find_elements_by_class_name("itemprop")
#[3]/td[4]/table/tbody/tr/td[5]/a


count=1
innerLink="";


for eachLink in loadMore:

    if(eachLink.tag_name):
        innerLink=eachLink.get_attribute('href') == 'html';
        print (innerLink);
    count = count + 1;
print (count)


