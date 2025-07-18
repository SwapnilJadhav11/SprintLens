import React, { useState, useEffect } from "react";
import { getChannels, generateSummary } from "../services/api";

const Dashboard = () => {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [channels, setChannels] = useState([]);
  const [selectedChannel, setSelectedChannel] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      const channelsData = await getChannels();
      setChannels(channelsData);
      if (channelsData.length > 0) {
        setSelectedChannel(channelsData[0].id);
      }
    } catch (err) {
      setError("Failed to fetch channels");
      console.error(err);
    }
  };

  const handleGenerateSummary = async () => {
    if (!selectedChannel) {
      setError("Please select a channel");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const summaryText = await generateSummary(selectedChannel, 7);
      setSummary(summaryText);
    } catch (err) {
      setError("Failed to generate summary");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getChannelName = (channelId) => {
    const channel = channels.find(ch => ch.id === channelId);
    return channel ? channel.name : "";
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4">
      <h1 className="text-3xl font-bold mb-6 text-center">SprintLens Dashboard</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Slack Integration</h2>
        <div className="flex items-center gap-4 mb-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Channel
            </label>
            <select
              value={selectedChannel}
              onChange={(e) => setSelectedChannel(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {channels.map((channel) => (
                <option key={channel.id} value={channel.id}>
                  #{channel.name}
                </option>
              ))}
            </select>
          </div>
          <button
            className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 disabled:opacity-50"
            onClick={handleGenerateSummary}
            disabled={loading || !selectedChannel}
          >
            {loading ? "Generating..." : "Generate Summary"}
          </button>
        </div>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">
          Sprint Summary {selectedChannel && `- #${getChannelName(selectedChannel)}`}
        </h2>
        <div className="bg-gray-50 p-4 rounded-md min-h-[200px]">
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <span className="ml-2">Generating summary...</span>
            </div>
          ) : summary ? (
            <div className="whitespace-pre-wrap">{summary}</div>
          ) : (
            <span className="text-gray-400">
              Click "Generate Summary" to create an AI-powered sprint summary.
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
