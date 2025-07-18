import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Slack API calls
export const getChannels = async () => {
  try {
    const response = await api.get('/api/slack/channels');
    return response.data.channels;
  } catch (error) {
    console.error('Error fetching channels:', error);
    throw error;
  }
};

export const getMessages = async (channelId, days = 7) => {
  try {
    const response = await api.get(`/api/slack/messages?channel_id=${channelId}&days=${days}`);
    return response.data.messages;
  } catch (error) {
    console.error('Error fetching messages:', error);
    throw error;
  }
};

// Summary API calls
export const generateSummary = async (channelId, days = 7, includeGitHub = false, includeJira = false, jiraProjectKey = null) => {
  try {
    const response = await api.post('/api/summary/generate', {
      channel_id: channelId,
      days: days,
      include_github: includeGitHub,
      include_jira: includeJira,
      jira_project_key: jiraProjectKey
    });
    return response.data.summary;
  } catch (error) {
    console.error('Error generating summary:', error);
    throw error;
  }
};

// GitHub API calls
export const getGitHubData = async (days = 7) => {
  try {
    const response = await api.get(`/api/github/repository?days=${days}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
    throw error;
  }
};

export const createGitHubIssue = async (title, body, labels = []) => {
  try {
    const response = await api.post('/api/github/issues', {
      title,
      body,
      labels
    });
    return response.data;
  } catch (error) {
    console.error('Error creating GitHub issue:', error);
    throw error;
  }
};

// Jira API calls
export const getJiraProjects = async () => {
  try {
    const response = await api.get('/api/jira/projects');
    return response.data.projects;
  } catch (error) {
    console.error('Error fetching Jira projects:', error);
    throw error;
  }
};

export const getJiraIssues = async (projectKey, days = 7) => {
  try {
    const response = await api.get(`/api/jira/issues?project_key=${projectKey}&days=${days}`);
    return response.data.issues;
  } catch (error) {
    console.error('Error fetching Jira issues:', error);
    throw error;
  }
};

// Bot API calls
export const postSummaryToSlack = async (channelId, summary) => {
  try {
    const response = await api.post('/api/bot/post-summary', {
      channel_id: channelId,
      summary
    });
    return response.data;
  } catch (error) {
    console.error('Error posting summary to Slack:', error);
    throw error;
  }
};

export const postWeeklySummary = async (channelId, days = 7) => {
  try {
    const response = await api.post('/api/bot/weekly-summary', {
      channel_id: channelId,
      days
    });
    return response.data;
  } catch (error) {
    console.error('Error posting weekly summary:', error);
    throw error;
  }
};

export default api;
