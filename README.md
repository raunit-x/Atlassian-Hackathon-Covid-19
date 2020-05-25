# Atlassian Hack@Home Final Round Winning Submission
<h3><b>1. The Dash Web App with Real Time Data Visualizations</b></h3>   
<img src = '/Covid 19 Dash App/Images/Screenshot 2020-05-25 at 12.04.18 PM.png' width = 900>
<img src = '/Covid 19 Dash App/Images/Screenshot 2020-05-25 at 12.04.31 PM.png' width = 900>
<img src = '/Covid 19 Dash App/Images/Screenshot 2020-05-25 at 12.04.57 PM.png' width = 900>
<img src = '/Covid 19 Dash App/Images/Screenshot 2020-05-25 at 12.05.11 PM.png'width = 900>
<ul>
  <li> A <a href="https://plotly.com/dash/">Dash</a> webapp with all the plots rendered using <a href="https://plotly.com/">plotly</a>.</li>
  <li>The data is fetched using <code>pandas</code> from the <a href="https://github.com/CSSEGISandData/COVID-19">John Hopkins Universtiy Github Repo</a> which is updated daily.</li>
</ul>

<h3><b>2. The Covid Info Store </b></h3> 
<img src = '/Covid 19 Dash App/Images/Screenshot 2020-05-25 at 12.05.50 PM.png' width = 900>
<ul>
  <li> It shows one of the best articles on COVID-19.</li>
  <li> Have to add a ranking algorithm to improve upon the recommendations.</li>
</ul>

<h3><b>3. Slack Bot </b></h3> 
<img src = 'Slack Notification Bot/Images/slackSS.png' width = 900>
<ul>
  <li> It updates the user directly on Slack on the changes in the COVID-19 cases in India.</li>
  <li>Using <code>BeautifulSoup</code> the data is directly scraped from the official <a href="https://www.mohfw.gov.in/">Indian Government Data</a></li>
  <li> Any changes in the number of cases is reported along with the same for all States/UT</li>
  <li> To add this to your own slack:
    <ol>
      <li>Configure your custom <a href = "https://api.slack.com/start">slack app</a> to a specific channel where you want the upates.</li>
      <li> Add your own <a href = "https://api.slack.com/messaging/webhooks">webhook</a> url in the code.</li>
    </ol>
    </li>

</ul>

# TODO
<ol>
  <li>Add a <code>plotly express scatter map_box</code> specifically for India.</li>
  <li>Add more visualizations for more specific data.</li>
  <li>Deploy the webapp using <code>Heroku</code>.</li>
  <li>Work on the <code>UI</code> of The Covid Info Store.</li>
  <li>Add a dynamic addition of curated articles for everyone to read on COVID-19 from official sources.</li>
</ol>
