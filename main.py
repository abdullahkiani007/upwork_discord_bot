import discord
from discord.ext import commands
from discord.ext.commands import Bot
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv()
prevUrl  = []



def scrape_jobs():
    print("Fetchning Jobs \n")
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    options.add_argument('--headless')  # Run without opening a browser window
    driver = webdriver.Firefox(options=options)

    url = 'https://www.upwork.com/nx/jobs/search/?q=react&sort=recency&payment_verified=1'
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    # Now you can use BeautifulSoup to parse page_source as before
    soup = BeautifulSoup(page_source, 'html.parser')


    job_sections = soup.find_all('section', {'data-test': 'JobTile'})
    if len(job_sections) > 0:
        print("Total jobs :" + str(len(job_sections)))
        for job_section in job_sections:
            # Extract job link
            job_link_element = job_section.find('a', {'data-test': 'UpLink'})

            job_unique_id = job_link_element['href'].split('~')[1]

            # Generate the new URL with the unique identifier
            new_url = f"https://www.upwork.com/jobs/~{job_unique_id}"

            if new_url not in prevUrl:
                prevUrl.append(new_url)
                # Extract job title
                title_element = job_section.find('h3', class_='job-tile-title')
                job_title = title_element.a.text.strip()

                # Extract job description
                description_element = job_section.find('span', {'data-test': 'job-description-text'})
                job_description = description_element.get_text(strip=True)

                # Extract job skills
                skills_elements = job_section.find_all('a', {'data-test': 'attr-item'})
                job_skills = [skill.text.strip() for skill in skills_elements]
                print("Job Title:", job_title)

                return {'status': True, 'data':{
                    'title': job_title,
                    'description': job_description,
                    'skills': job_skills,
                    'link': new_url
                }}
            else:
                continue
            

    else:
        return {'status': False, 'data':{}}


intents = discord.Intents.default()  # Create a default intents object
intents.typing = True
intents.presences = True
intents.guild_messages = True
intents.message_content = True

bot = Bot(command_prefix='!', intents=intents)  # Pass intents to the Bot object




# Command to fetch and send job listings
@bot.command(name='fetch_jobs')
async def fetch_jobs(ctx):
    await ctx.send("Hang tight fetching jobs")
    job = scrape_jobs()  # Call your scraping function

    # Send job listings to Discord
    if job['status']:
        job = job['data']
        job_embed = discord.Embed(title=job['title'], description=job['description'])
        job_embed.add_field(name='Skills', value=', '.join(job['skills']), inline=False)
        job_embed.add_field(name='Link', value=job['link'], inline=False)

        await ctx.send(embed=job_embed)
    else:
        await ctx.send("No new jobs found")


#  2nd way to do it

client = discord.Client(intents=intents)

# Initialize Selenium WebDriver (executed in a separate thread)
def init_selenium():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
    options.add_argument('--headless')  # Run without opening a browser window
    driver = webdriver.Firefox(options=options)
    return driver

# Function to perform Selenium actions (executed in a separate thread)
def perform_selenium_actions(driver):
    
    url = 'https://www.upwork.com/nx/jobs/search/?q=react&sort=recency&payment_verified=1'
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    # Now you can use BeautifulSoup to parse page_source as before
    soup = BeautifulSoup(page_source, 'html.parser')


    job_sections = soup.find_all('section', {'data-test': 'JobTile'})
    if len(job_sections) > 0:
        print("Total jobs :" + str(len(job_sections)))
        for job_section in job_sections:
            # Extract job link
            job_link_element = job_section.find('a', {'data-test': 'UpLink'})

            job_unique_id = job_link_element['href'].split('~')[1]

            # Generate the new URL with the unique identifier
            new_url = f"https://www.upwork.com/jobs/~{job_unique_id}"

            if new_url not in prevUrl:
                prevUrl.append(new_url)
                # Extract job title
                title_element = job_section.find('h3', class_='job-tile-title')
                job_title = title_element.a.text.strip()

                # Extract job description
                description_element = job_section.find('span', {'data-test': 'job-description-text'})
                job_description = description_element.get_text(strip=True)

                # Extract job skills
                skills_elements = job_section.find_all('a', {'data-test': 'attr-item'})
                job_skills = [skill.text.strip() for skill in skills_elements]
                print("Job Title:", job_title)

                return {'status': True, 'data':{
                    'title': job_title,
                    'description': job_description,
                    'skills': job_skills,
                    'link': new_url
                }}
            else:
                continue
            

    else:
        return {'status': False, 'data':{}}



@bot.command(name='selenium')
async def selenium(ctx):
    await ctx.send('Running Selenium...')
    
    # Use run_in_executor to run Selenium functions asynchronously
    with concurrent.futures.ThreadPoolExecutor() as executor:
        driver = await asyncio.get_event_loop().run_in_executor(None, init_selenium)
        job_data = await asyncio.get_event_loop().run_in_executor(executor, perform_selenium_actions, driver)
        # driver.quit()  # Remember to close the driver
    
    if job_data['status']:
        job_data = job_data['data']
        # Send the scraped job data as an embed
        job_embed = discord.Embed(title=job_data['title'], description=job_data['description'])
        job_embed.add_field(name='Skills', value=', '.join(job_data['skills']), inline=False)
        job_embed.add_field(name='Link', value=job_data['link'], inline=False)
        await ctx.send(embed=job_embed)

        await ctx.send('Selenium task complete!')
    else:
        await ctx.send('No new jobs found')


# Function to fetch and send job listings
async def fetch_and_send_jobs(channel):
    while True:
        await asyncio.sleep(300)  # Wait for an interval of 1 hour (adjust as needed)
        
        job = scrape_jobs()  # Call your scraping function

        # Send job listings to Discord
        if job['status']:
            job = job['data']
            job_embed = discord.Embed(title=job['title'], description=job['description'])
            job_embed.add_field(name='Skills', value=', '.join(job['skills']), inline=False)
            job_embed.add_field(name='Link', value=job['link'], inline=False)
            
            await channel.send(embed=job_embed)
        else:
            await channel.send("No new jobs found")
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # Get the desired channel (replace CHANNEL_ID with the actual channel ID)
    channel = bot.get_channel(1137816662461120512)
    
    # Start the fetch_and_send_jobs coroutine
    bot.loop.create_task(fetch_and_send_jobs(channel))




bot.run(os.environ['DISCORD_API_TOKEN'])
