package com.example.spring_project;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.openqa.selenium.By;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.concurrent.TimeUnit;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class HomePageTest {
    @LocalServerPort
    private int port;

    private static HtmlUnitDriver browser;

    @BeforeClass
    public static void setup() {
        browser = new HtmlUnitDriver();
        browser.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    }

    @AfterClass
    public static void teardown() {
        browser.quit();
    }

    @Test
    public void testTitle() {
        String homePage = "http://localhost:" + port;
        browser.get(homePage);

        String titleText = browser.getTitle();
        assertEquals("Hospital Management System", titleText);
    }

    @Test
    public void testH1Text() {
        String homePage = "http://localhost:" + port;
        browser.get(homePage);

        // Проверка текста в элементе h1
        String h1Text = browser.findElement(By.tagName("h1")).getText();
        assertEquals("Добро пожаловать в HealthHub!", h1Text);
    }

    @Test
    public void testNavigationLinks() {
        String homePage = "http://localhost:" + port;
        browser.get(homePage);

        String[] expectedLinks = {"О нас", "Услуги", "Персонал", "График", "Отзывы", "Лекарства"};
        boolean isEmpty = false;
        for (String linkText : expectedLinks) {
            isEmpty = browser.findElements(By.linkText(linkText)).isEmpty();
            assertTrue("Ссылка (" + linkText + ") должна присутствовать.", !isEmpty);
        }
    }
}
