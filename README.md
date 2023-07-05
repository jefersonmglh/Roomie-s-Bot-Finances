# Roomie's Bot Finances

Roomie's Bot Finances is a Telegram bot application designed to assist in managing the finances of a house shared by roommates. With this application, you can easily add and track expenses submitted by users.

## Key Features

- **Add Expenses**: Users can submit expense details, including description and amount, directly to the Telegram bot.
- **Expense Database**: All expenses are stored in a secure database, ensuring the integrity of financial records.
- **Monthly Closing**: At the end of each month, Roomie's Bot Finances allows you to close the finances by calculating the fair division of expenses among all the housemates.
- **Automatic Splitting**: Based on the number of roommates, the application automatically calculates the proportional division of expenses, simplifying the process of splitting bills.
- **Expense Visualization**: In addition to its features, Roomie's Bot Finances also offers the option to visualize expenses through charts. The app provides two types of charts that help you analyze and understand the expenditure patterns.

   1. **User-based Expense Chart**: This chart illustrates the expenses incurred by each individual roommate. It allows you to identify the spending behavior of each person, facilitating discussions and promoting transparency within the shared household finances.

   2. **Description-based Expense Chart**: This chart showcases the distribution of expenses based on different categories or descriptions. It enables you to see which types of expenses contribute the most to your overall spending, assisting you in identifying areas where cost-cutting measures can be implemented.

By incorporating these graphical representations, Roomie's Bot Finances enhances your financial management experience, providing a visual overview of your expenditure data. Gain valuable insights into your spending habits and foster a more informed approach to budgeting and expense tracking.

## Installation

1. Create a Python Virtual Environment. Refer to this guide: [How to Setup Virtual Environments in Python](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
2. Install all the necessary packages listed in requirements.txt. Use the following command: `pip install -r requirements.txt`. Learn more: [Installing Packages Using a Requirements File](https://learnpython.com/blog/python-requirements-file/#:~:text=Use%20the%20pip%20install%20%2Dr,up%20to%20date%20and%20accurate.)
3. Create a MongoDB Atlas account (if you don't have one), obtain the MongoDB Authentication, and paste it into the .env file. See this guide: [MongoDB Atlas - Creating Database Users for Atlas Deployments](https://www.mongodb.com/docs/atlas/app-services/users/)
4. Create a Telegram Bot, obtain the Bot's Token, and paste it into the .env file. Follow the instructions here: [How to Create a Telegram Bot](https://helpdesk.bitrix24.com/open/17622486/)
5. In the Python Environment Terminal, run the following command:

   ```bash
   python3 bot_main.py 
   
6. Enjoy!

Notes:

- This was my first app that I developed independently while learning Python. I hold it dear and decided to make it public. However, I welcome any feedback you may have!
