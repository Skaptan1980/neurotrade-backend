#!/bin/bash

# Set Variables
APP_NAME="neurotrade-api"
GIT_REPO="https://github.com/your-username/neurotrade-backend.git"
RENDER_DEPLOY_URL="https://api.render.com/deploy/srv-XXXXXX"

# Install Required Dependencies
pip install -r requirements.txt

# Initialize Git if not already initialized
git init
git remote add origin $GIT_REPO
git add .
git commit -m "Deploying NeuroTrade API"
git push -u origin main

# Deploy to Render
curl -X POST $RENDER_DEPLOY_URL -H "Accept: application/json" -H "Authorization: Bearer YOUR_RENDER_API_KEY" -d '{}'

# Deploy to Heroku (Alternative)
# heroku create $APP_NAME
# heroku git:remote -a $APP_NAME
# git push heroku main
# heroku config:set ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
# heroku config:set AI_TRADE_API_URL=your_ai_api_url
# heroku config:set SENTIMENT_API_URL=your_sentiment_api_url
# heroku config:set PORTFOLIO_ANALYTICS_API=your_portfolio_analytics_api
# heroku open
