import React, { useState, useEffect } from "react";
import { getChannels, generateSummary, getBotResponse, getCalendarEvents } from "../services/api";

const Dashboard = () => {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [channels, setChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState("");
  const [error, setError] = useState("");
  const [botResponse, setBotResponse] = useState("");
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [includeCalendar, setIncludeCalendar] = useState(false);

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      const channelsData = await getChannels();
      setChannels(channelsData);
      if (channelsData.length > 0) {
        setSelectedChannel(channelsData[0].id);
      } else {
        // If no channels, use a default channel ID for testing
        setSelectedChannel("C096K8MU2LC");
      }
    } catch (err) {
      setError("Failed to fetch channels");
      console.error(err);
    }
  };

  const handleGenerateSummary = async () => {
    setLoading(true);
    setError("");
    try {
      // Include GitHub and optionally calendar
      const summaryText = await generateSummary(selectedChannel, 7, true, false, includeCalendar, null);
      setSummary(summaryText);
    } catch (err) {
      setError("Failed to generate summary: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBotCommand = async (command) => {
    try {
      const response = await getBotResponse(selectedChannel, "U123456", `@SprintLens ${command}`);
      setBotResponse(response);
    } catch (err) {
      setError("Failed to get bot response: " + err.message);
      console.error(err);
    }
  };

  const handleFetchCalendar = async () => {
    try {
      const events = await getCalendarEvents(7);
      setCalendarEvents(events);
    } catch (err) {
      setError("Failed to fetch calendar events: " + err.message);
      console.error(err);
    }
  };

  const getChannelName = (channelId) => {
    const channel = channels.find(ch => ch.id === channelId);
    return channel ? channel.name : "";
  };

    return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="max-w-6xl mx-auto py-8 px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            SprintLens Dashboard
          </h1>
          <p className="text-gray-300">AI-Powered Sprint Summaries</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Control Panel */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4 text-blue-400">Configuration</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Slack Channel
                  </label>
                  <select
                    value={selectedChannel}
                    onChange={(e) => setSelectedChannel(e.target.value)}
                    className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
                  >
                    {channels.length > 0 ? (
                      channels.map((channel) => (
                        <option key={channel.id} value={channel.id}>
                          #{channel.name}
                        </option>
                      ))
                    ) : (
                      <option value="C096K8MU2LC">#general (Default)</option>
                    )}
                  </select>
                </div>

                <div className="flex items-center space-x-4">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      defaultChecked={true}
                      className="rounded border-gray-600 text-blue-500 focus:ring-blue-500 bg-gray-700"
                    />
                    <span className="ml-2 text-sm text-gray-300">Include GitHub</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={includeCalendar}
                      onChange={(e) => setIncludeCalendar(e.target.checked)}
                      className="rounded border-gray-600 text-blue-500 focus:ring-blue-500 bg-gray-700"
                    />
                    <span className="ml-2 text-sm text-gray-300">Include Calendar</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded border-gray-600 text-blue-500 focus:ring-blue-500 bg-gray-700"
                    />
                    <span className="ml-2 text-sm text-gray-300">Include Jira</span>
                  </label>
                </div>

                <button
                  className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={handleGenerateSummary}
                  disabled={loading}
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Generating...
                    </div>
                  ) : (
                    "🚀 Generate Summary"
                  )}
                </button>
              </div>

              {error && (
                <div className="mt-4 bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg">
                  {error}
                </div>
              )}

              {/* Bot Commands Section */}
              <div className="mt-6 pt-6 border-t border-gray-700">
                <h3 className="text-lg font-semibold mb-3 text-blue-400">Slack Bot Commands</h3>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => handleBotCommand('status')}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm transition-colors"
                  >
                    📊 Status
                  </button>
                  <button
                    onClick={() => handleBotCommand('help')}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm transition-colors"
                  >
                    ❓ Help
                  </button>
                  <button
                    onClick={() => handleBotCommand('summary')}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm transition-colors"
                  >
                    📋 Summary
                  </button>
                  <button
                    onClick={() => handleBotCommand('remind')}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded text-sm transition-colors"
                  >
                    🔔 Remind
                  </button>
                </div>
                
                {botResponse && (
                  <div className="mt-4 p-3 bg-gray-900 rounded border border-gray-700">
                    <h4 className="text-sm font-medium text-blue-400 mb-2">Bot Response:</h4>
                    <div className="text-sm text-gray-300 whitespace-pre-wrap">{botResponse}</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Summary Display */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4 text-blue-400">
                Sprint Summary
                {selectedChannel && channels.length > 0 && (
                  <span className="text-gray-400 ml-2">- #{getChannelName(selectedChannel)}</span>
                )}
              </h2>
              
              <div className="bg-gray-900 p-6 rounded-lg min-h-[400px] border border-gray-700">
                {loading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                      <p className="text-gray-400">Generating AI-powered summary...</p>
                    </div>
                  </div>
                ) : summary ? (
                  <div className="prose prose-invert max-w-none">
                    <div className="whitespace-pre-wrap text-gray-200 leading-relaxed">{summary}</div>
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-full text-center">
                    <div>
                      <div className="text-6xl mb-4">📊</div>
                      <p className="text-gray-400 text-lg">
                        Click "Generate Summary" to create an AI-powered sprint summary.
                      </p>
                      <p className="text-gray-500 text-sm mt-2">
                        This will analyze your Slack, GitHub, and Jira data.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
