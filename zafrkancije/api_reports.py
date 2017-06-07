from selenium import webdriver

driver = webdriver.Chrome(r"C:\TFS\RatingAPIReports\RatingAPIReports.Tests\bin\Debug\chromedriver.exe")
driver.get("https://t.ratingapireporting.devop.vertafore.com/v1/Account/Login")
driver.find_element_by_xpath(r'//*[@id="Email"]').send_keys("APIAdmin@vertafore.com")
driver.find_element_by_xpath(r'//*[@id="Password"]').send_keys("Verta4!")

driver.find_element_by_xpath(r'//*[@id="loginForm"]/form/div[4]/div/input').click()
driver.switch_to.frame(0)

element = driver.find_element_by_xpath("//*[contains(text(), 'Rating Events Report')]").get_attribute('class')
while element.tag_name != 'tbody':
    parent = driver.execute_script("return arguments[0].parentNode;", element)
    element = parent
rating_event_element_parent = driver.execute_script("return arguments[0].parentNode;", element)
#A388b33ff3f3e4faab6d6a2cdf3b2baf842c

elem = driver.find_element_by_xpath("//a[@onclick=\"var rp=$get('ReportViewer1_ctl09_ReportControl');if(rp&&rp.control)rp.control.InvokeReportAction('Sort','73iT0_A');return false;\"]")
