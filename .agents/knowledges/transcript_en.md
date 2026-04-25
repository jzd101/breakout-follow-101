[Transcript] I created the most realistic trading system right now…
Channel: ORC Crypto
Video Length: 28:53 minutes

Introduction and System Concept
[00:00] The 1,000 percent profit everyone sees on the video thumbnail, all the information and trading methods, and various concepts that everyone will see in the following clip, are all real information, provable, and statistically reproducible. A trading system that doesn't guess or predict whether it will go up or down, but we will use pure mathematics, numbers, and statistics to tell which way to trade. I will take everyone by the hand and try to do it together. To prove it's the most tangible, I backtested every candle for 2 full years to prove that a 1,000% profit is a real possibility, which everyone can watch in this clip, including how to reach the point I'm talking about with true understanding and the right mindset to elevate everyone into better traders together.

[00:50] And so you don't miss content from ORC Crypto, any member who wants to follow news or contact me directly can go and say hello on the Facebook page here. Or if you want a trade setup, signal, or "hint," it's in the Discord group, which is free to join. Inside, there will be discussions between me and all my friends on the ORC Crypto channel, as well as important financial world news. But if anyone likes watching short, concise clips, TikTok and Instagram are two other channels where I post short clips all the time. Whichever app you use often, go watch from that platform. Follow and come talk to me; see you there.

[01:36] Hello to all traders. Welcome back to ORC Crypto. This clip is another one I've put my heart into and it took a long time to complete because I had to try and error countless times through both backtesting and forward testing. So, if everyone watches this clip of mine until the end, it's equivalent to saving several months of your life. The information in this clip is quite extensive, with detailed and thorough content. So, I want everyone to watch this clip until the end without skipping, because if there's any part you're unsure about or don't understand, you can note the minute and comment below. I promise I'll come and answer as much as possible because this clip has quite a lot of detail, but I believe it's not beyond everyone's ability to understand. Even if you're not a pro trader or a beginner just starting, you can understand because I'll use simple terms, explain in detail, and provide easy examples.

5 Workflow Steps
[02:31] In this clip, the testing and creation of this system will be based on a cryptocurrency pair like Bitcoin. But don't misunderstand and think it only works for Cryptocurrency, because it can be used for everything, whether it's Forex, Gold, Stocks, commodities like crude oil, or corn. But for ease of extracting data and various testing variables, I'll use Bitcoin. If anyone already trades something else, you can apply it directly.

[03:01] Alright, this clip will be a consolidation of the right ideas, including the mindset I've taught on this channel; almost everything will be adjusted and used in this clip. So we must understand first what our workflow and the order of explanation in this clip will be:
1. Find the asset we want to test or trade (in this case, Bitcoin).
2. Find a trading system that can trade this asset (SMC, ICT, Elliott Wave, etc.). A good system must be tangible and always reproducible. Rules must be strong enough not to involve emotions.
3. Define or limit our capital and Risk (e.g., 10,000 Baht capital, risk 1%, meaning you can lose a maximum of 100 Baht per time).
4. Perform Backtesting and Forward testing to know how this system performs against the past and future.
5. Take action for real.

Indicator Settings in TradingView
[07:23] Let's start the setup process. Have everyone open TradingView. Adjust the Time Frame to 1 hour (a medium timeframe for a midterm trend) and add these Indicators:
- EMA (Exponential Moving Average): Adjust the Length to 200 (white line) to divide the Trend zones.
- Bollinger Bands: Use standard values (Length 20, StdDev 2).
- Volume: Turn on the Moving Average of Volume too (Style > Volume MA).
- ATR (Average True Range): For setting Stop Loss points (Length 14).

Breakout Follow Trend Strategy
[11:11] This strategy is called Breakout Follow Trend, which is following the big players' push and taking small bites with a Risk Reward (RR) of 2.0.

Long Conditions:
- The candle must stand above the EMA 200 line (Uptrend).
- The candle must break through the Upper Band of the Bollinger Bands.
- Important: When it breaks, the Volume below must be higher than average (higher than the yellow MA line in the Volume section).
- When the candle closes according to the conditions, open a Long order immediately.

Setting Stop Loss and Take Profit:
- Stop Loss: Use the ATR value at that candle multiplied by 2 (ATR x 2).
- Take Profit: Set the profit target at RR = 2.0.

Backtesting and 2-Year Results
[17:23] In backtesting, I didn't click manually but used Python to pull API data (CCXT) for a 2-year backtest using an initial capital of 3,000 USD, risking 3% per time with Compounding.

Calculation Results:
- Initial Capital: 3,000 USD
- Ending Balance: 74,020.4 USD
- Profit (Net PNL): 71,020.4 USD
- ROI: 2,367.35% (after fees)
- Total Trades: 1,389
- Win Rate: 36.72% (consistent with an RR 1:2 system)
- Realized RR: Approximately 1:1.99

Forward Testing and Membership System
[22:22] After backtesting, we must forward test with the real market. I ran a bot on a Server to see if the system works as tested. Anyone interested in having a trading bot but can't code, the channel now has a Membership system for 300 Baht per month, teaching Auto Trading with Python and providing scripts to copy and paste.

Setting Alerts for Manual Traders
[25:25] For those not using a bot, set Alerts in TradingView:
- Long: Set Price > Crossing Up > Bollinger Bands (Upper) > Once per bar close.
- Short: Set Price > Crossing Down > Bollinger Bands (Lower) > Once per bar close.
- When alerted, check EMA 200 and Volume conditions before entering the trade.

[28:13] Conclusion of the clip: This system focuses on following trends when big players enter, causing a short-term volume spike. If anyone has questions, leave a comment. For today, goodbye.
