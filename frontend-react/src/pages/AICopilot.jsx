import { useState, useEffect, useRef } from "react";
import {
  Box, Paper, Typography, TextField, Button, Chip,
  CircularProgress, Divider, Avatar, IconButton, Tooltip,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import API from "../services/api";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import PersonIcon from "@mui/icons-material/Person";
import DeleteOutlineIcon from "@mui/icons-material/DeleteForever";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import PageHeader from "../components/PageHeader";

//const API = "http://127.0.0.1:8000";

const WELCOME = {
  role: "assistant",
  text: "Hello! I'm the **VisionIQ AI Copilot**.\n\nI can answer questions about your SAP PM data — equipment risk, failures, backlog, MTTR, PM compliance, and more.\n\nType **help** to see all supported questions, or try one of the suggestions below.",
  recommendations: [],
  assets: [],
};

function renderMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br/>");
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  const [copied, setCopied] = useState(false);

  const copy = () => {
    navigator.clipboard.writeText(msg.text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 1.5,
        mb: 2.5,
        flexDirection: isUser ? "row-reverse" : "row",
        alignItems: "flex-start",
      }}
    >
      <Avatar
        sx={{
          width: 34, height: 34, flexShrink: 0,
          bgcolor: isUser ? "primary.main" : "secondary.main",
        }}
      >
        {isUser ? <PersonIcon sx={{ fontSize: 18 }} /> : <SmartToyIcon sx={{ fontSize: 18 }} />}
      </Avatar>

      <Box sx={{ maxWidth: "80%" }}>
        <Paper
          elevation={0}
          sx={{
            p: 2, borderRadius: 2,
            bgcolor: isUser ? "primary.main" : "background.paper",
            border: isUser ? "none" : "1px solid",
            borderColor: "divider",
          }}
        >
          <Typography
            variant="body2"
            component="div"
            sx={{ lineHeight: 1.7 }}
            dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.text) }}
          />

          {/* Related assets chips */}
          {msg.assets?.length > 0 && (
            <Box sx={{ mt: 1.5, display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {msg.assets.map((a) => (
                <Chip key={a} label={a} size="small" variant="outlined" color="primary" />
              ))}
            </Box>
          )}

          {/* Recommendations */}
          {msg.recommendations?.length > 0 && (
            <Box sx={{ mt: 1.5 }}>
              <Typography variant="caption" color="text.secondary" fontWeight={600}>
                RECOMMENDED ACTIONS
              </Typography>
              {msg.recommendations.map((r, i) => (
                <Typography key={i} variant="caption" display="block" sx={{ mt: 0.3, pl: 1 }}>
                  → {r}
                </Typography>
              ))}
            </Box>
          )}
        </Paper>

        {!isUser && (
          <Tooltip title={copied ? "Copied!" : "Copy response"}>
            <IconButton size="small" onClick={copy} sx={{ mt: 0.3, opacity: 0.5 }}>
              <ContentCopyIcon sx={{ fontSize: 14 }} />
            </IconButton>
          </Tooltip>
        )}
      </Box>
    </Box>
  );
}

export default function AICopilot() {
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/copilot/suggest`)
      .then((r) => r.json())
      .then((d) => setSuggestions(d.suggestions ?? []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (question) => {
    const q = (question || input).trim();
    if (!q) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/copilot/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer,
          assets: data.related_assets ?? [],
          recommendations: data.recommendations ?? [],
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "⚠️ Unable to reach the backend. Please ensure the server is running.", assets: [], recommendations: [] },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clear = () => setMessages([WELCOME]);

  return (
    <Box sx={{ p: 3, height: "calc(100vh - 90px)", display: "flex", flexDirection: "column" }}>
      <PageHeader
        title="AI Copilot"
        subtitle="Ask anything about your SAP PM maintenance data"
        breadcrumbs={["VisionIQ", "AI Copilot"]}
        actions={
          <Tooltip title="Clear conversation">
            <IconButton onClick={clear} size="small">
              <DeleteOutlineIcon />
            </IconButton>
          </Tooltip>
        }
      />

      {/* Chat window */}
      <Paper
        elevation={0}
        sx={{
          flex: 1, overflow: "auto", p: 2.5, mb: 2,
          border: "1px solid", borderColor: "divider", borderRadius: 3,
          minHeight: 0,
        }}
      >
        {messages.map((msg, i) => (
          <Message key={i} msg={msg} />
        ))}

        {loading && (
          <Box sx={{ display: "flex", gap: 1.5, alignItems: "center", mb: 2 }}>
            <Avatar sx={{ width: 34, height: 34, bgcolor: "secondary.main" }}>
              <SmartToyIcon sx={{ fontSize: 18 }} />
            </Avatar>
            <Paper elevation={0} sx={{ p: 1.5, borderRadius: 2, border: "1px solid", borderColor: "divider" }}>
              <CircularProgress size={16} sx={{ mr: 1 }} />
              <Typography variant="caption" color="text.secondary">Analyzing your data...</Typography>
            </Paper>
          </Box>
        )}
        <div ref={bottomRef} />
      </Paper>

      {/* Suggested questions */}
      {messages.length === 1 && suggestions.length > 0 && (
        <Box sx={{ mb: 1.5 }}>
          <Typography variant="caption" color="text.secondary" fontWeight={600} sx={{ mb: 0.8, display: "block" }}>
            SUGGESTED QUESTIONS
          </Typography>
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.8 }}>
            {suggestions.slice(0, 6).map((s) => (
              <Chip
                key={s} label={s} size="small" variant="outlined"
                onClick={() => send(s)}
                sx={{ cursor: "pointer", "&:hover": { bgcolor: "action.hover" } }}
              />
            ))}
          </Box>
        </Box>
      )}

      {/* Input row */}
      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Ask about equipment risk, failures, backlog, MTTR, PM compliance..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
          disabled={loading}
          sx={{ "& .MuiOutlinedInput-root": { borderRadius: 3 } }}
          multiline
          maxRows={3}
        />
        <Button
          variant="contained"
          onClick={() => send()}
          disabled={loading || !input.trim()}
          sx={{ borderRadius: 3, minWidth: 52, px: 2 }}
        >
          <SendIcon />
        </Button>
      </Box>
    </Box>
  );
}
