"use client";

import { useState } from "react";
import { useConversation } from "@elevenlabs/react";
import { Mic } from "lucide-react";
import Bannerbg from "../../../public/image/banner.png";
import bannerMiddle from "../../../public/image/bannerMiddle.png";
import logo from "../../../public/image/logo.png";
import { Link } from "react-router-dom";

export default function AiQuestion() {
  const [isRecording, setIsRecording] = useState(false);

  const agentId = "agent_2401k1n3b0b5ed0s402cvcnvq2dn";
  const voiceId = "cjVigY5qzO86Huf0OWal";

  // ElevenLabs hook
  const conversationHook = useConversation({
    onConnect: () => console.log("Connected"),
    onDisconnect: () => console.log("Disconnected"),
    onMessage: (msg) => console.log("AI response:", msg),
    onError: (err) => console.error("Error:", err),
    onAudio: (audioChunk) => {
      // Play AI audio safely
      const audioBlob = new Blob([audioChunk], { type: "audio/mpeg" });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    },
    onDebug: (info) => {},
  });

  const toggleRecording = async () => {
      try {
        if (!isRecording) {
          await navigator.mediaDevices.getUserMedia({ audio: true });
          await conversationHook.startSession({
            agentId,
            connectionType: 'webrtc',
          });
          setIsRecording(true);
        } else {
          if (conversationHook.status === 'connected') {
            try {
              await conversationHook.endSession();
            } catch (err) {
              // Suppress harmless WebRTC cleanup errors
              const isWebRTCCleanupError = 
                err?.message?.includes("RTCRtpSender") ||
                err?.message?.includes("removeTrack") ||
                err?.message?.includes("connection state mismatch") ||
                err?.name === "TypeError";

              if (isWebRTCCleanupError) {
                // Silently ignore - these are expected during cleanup
                console.debug("WebRTC cleanup (harmless):", err?.message);
              } else {
                throw err; // Re-throw unexpected errors
              }
            }
          }
          setIsRecording(false);
        } 
      } catch (err) {
        console.error("Recording error:", err);
        setIsRecording(false);
      }
};


  return (
    <div
      className="bg-cover bg-center"
      style={{ backgroundImage: `url(${Bannerbg})` }}
    >
      <div className="bg-[linear-gradient(to_bottom_left,#0C4B4000,#E0ECE940,#FFFFFF)] min-h-screen">
        {/* Header */}
        <div className="px-30 pt-6 mx-auto flex justify-between items-center">
          <img src={logo} alt="Logo" className="md:h-14 h-10 w-auto" />
        </div>

        {/* Banner */}
        <div>
          <img
            src={bannerMiddle}
            className="w-full absolute h-50 md:top-[40%] top-[30%]"
            alt=""
          />
        </div>

        {/* Title */}
        <h1 className="text-teal-600 font-bold flex justify-center items-center text-2xl md:text-4xl italic mt-10 md:mt-20">
          Let's start your survey
        </h1>

        {/* Recording button */}
        <div className="px-4 max-w-4xl mx-auto mt-40 md:mt-60 w-full relative flex flex-col items-center space-y-4">
          <div className="relative">
            {isRecording && (
              <>
                <div className="absolute inset-0 rounded-full bg-emerald-400 opacity-20 animate-ping scale-150"></div>
                <div className="absolute inset-0 rounded-full bg-emerald-400 opacity-30 animate-pulse scale-125"></div>
                <div className="absolute inset-0 rounded-full bg-emerald-400 opacity-40 animate-pulse scale-110"></div>
              </>
            )}
            <button
              onClick={toggleRecording}
              className={`relative rounded-full md:h-30 h-18 w-18 md:w-30 transition-all duration-300 transform flex items-center justify-center cursor-pointer ${
                isRecording
                  ? "bg-gradient-to-br from-[#1D8C79] to-[#03493D] shadow-2xl shadow-emerald-500/50 scale-110 hover:scale-115"
                  : "bg-gradient-to-br from-[#1D8C79] to-[#03493D] shadow-xl shadow-gray-500/30 hover:shadow-2xl hover:shadow-gray-500/40 hover:scale-105"
              }`}
            >
              <Mic
                className={`h-10 w-10 text-white transition-all duration-200 ${
                  isRecording ? "animate-pulse" : ""
                }`}
              />
            </button>
          </div>
          {isRecording && (
            <p className="text-[#03493D] text-lg font-medium animate-pulse mt-6 flex items-center justify-center gap-2">
              <span className="w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
              Recording... Tap to stop
              <span className="w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
            </p>
          )}
        </div>

        {/* Feedback link */}
        <Link to="/feedback" className="flex justify-center mt-16 md:mt-32">
          <button className="px-14 py-3 rounded-full bg-gradient-to-t from-[#02362E] to-[#298F7D] text-gray-200 md:text-[20px] text-[12px]">
            Survey Feedback Overview
          </button>
        </Link>
      </div>
    </div>
  );
}
