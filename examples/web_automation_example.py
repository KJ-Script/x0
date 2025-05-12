"""
Example: Using Web Automation Tools

This example demonstrates how to use the web automation tools to:
1. Navigate to a website
2. Fill a form
3. Click buttons
4. Extract data
5. Take screenshots
"""

import asyncio
from exo.tools.tools.web_automation import (
    navigate_tool,
    fill_form_tool,
    click_tool,
    extract_tool,
    screenshot_tool
)

async def main():
    # Example: Automate a login process and extract data
    
    # 1. Navigate to the website
    print("Navigating to website...")
    result = await navigate_tool(url="https://example.com")
    print(f"Navigation result: {result}")
    
    # 2. Fill a login form
    print("\nFilling login form...")
    form_data = {
        "#username": "test_user",
        "#password": "test_pass"
    }
    result = await fill_form_tool(
        selector="form.login-form",
        data=form_data
    )
    print(f"Form filling result: {result}")
    
    # 3. Click the login button
    print("\nClicking login button...")
    result = await click_tool(selector="button[type='submit']")
    print(f"Click result: {result}")
    
    # 4. Extract data from the dashboard
    print("\nExtracting dashboard data...")
    selectors = {
        "username": ".user-profile .username",
        "balance": ".account-balance",
        "last_login": ".last-login-time"
    }
    result = await extract_tool(selectors=selectors)
    print(f"Extracted data: {result}")
    
    # 5. Take a screenshot
    print("\nTaking screenshot...")
    result = await screenshot_tool(
        selector=".dashboard-content",
        path="dashboard.png"
    )
    print(f"Screenshot result: {result}")

if __name__ == "__main__":
    asyncio.run(main()) 