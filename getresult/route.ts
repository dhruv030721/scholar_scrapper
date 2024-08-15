import { NextResponse } from "next/server";
import puppeteer from "puppeteer";
import path from "path";
import fs from "fs/promises";
import FormData from 'form-data';
import axios from 'axios';

export async function GET(request: Request) {
    let browser;

    try {
        browser = await puppeteer.launch({ headless: true });
        const page = await browser.newPage();

        await page.goto('https://www.gturesults.in/');

        // Wait for the select element with the specific id
        const selectId = 'ddlbatch';
        await page.waitForSelector(`select#${selectId}`);

        const sem6_result = ".....BPH SEM 6 - Regular (MAY 2024)";

        // Extract and filter options from the select element
        const filteredOptions = await page.evaluate((selectId, sem6_result) => {
            const select: any = document.querySelector(`select#${selectId}`);
            const options: any = Array.from(select.options).filter((option: any) => option.innerText.trim() === sem6_result);
            return options.map((option: { value: any; innerText: string; }) => ({
                value: option.value,
                text: option.innerText.trim()
            }));
        }, selectId, sem6_result);

        // if (filteredOptions) {
        //     //TODO: Send Mail
        // }

        const element = await page.$('#imgCaptcha');
        const boundingBox = await element.boundingBox();

        const savePath = path.join(__dirname, '../../../../../app/captchas/', 'screenshot.png');

        await page.screenshot({
            path: savePath,
            clip: {
                x: boundingBox.x,
                y: boundingBox.y,
                width: boundingBox.width,
                height: boundingBox.height
            }
        });

        const captchaImgBuffer = await fs.readFile(savePath);

        // Construct form-data
        const formData = new FormData();
        formData.append('captcha_image', captchaImgBuffer, {
            filename: 'captcha.png',
            contentType: 'image/png',
        });

        // Define the URL of the Flask API endpoint
        const flaskApiUrl = 'http://127.0.0.1:5000/api/get_captcha_value';

        // Use axios to send the form-data
        const response = await axios.post(flaskApiUrl, formData, {
            headers: formData.getHeaders(),
        });

        console.log(response.data);

        return NextResponse.json(response.data);
    } catch (error) {
        console.error('Error:', error);
        return NextResponse.error();
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}
