import { useState } from "react";
import { MessageCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ChatWindow } from "./ChatWindow";

export function Widget() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <AnimatePresence>
        {isOpen && <ChatWindow onClose={() => setIsOpen(false)} />}
      </AnimatePresence>

      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen((prev) => !prev)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-xl flex items-center justify-center z-[9999] hover:shadow-blue-600/25 hover:shadow-2xl transition-all"
        aria-label="Toggle digital twin chat"
      >
        <MessageCircle size={24} />
        {/* Optional glowing effect */}
        <span className="absolute inset-0 rounded-full animate-ping bg-blue-600/20 -z-10" style={{ animationDuration: '3s' }}></span>
      </motion.button>
    </>
  );
}
