// Main JavaScript for CMU Africa Student Project Hub

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Initialize popovers
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Chat functionality
  initializeChat();

  // Smooth scrolling for anchor links
  initializeSmoothScrolling();

  // Add fade-in animations
  initializeAnimations();

  // Initialize form enhancements
  initializeFormEnhancements();
});

// Chat functionality
function initializeChat() {
  const chatButton = document.getElementById("chatButton");
  const chatExpandable = document.getElementById("chatExpandable");
  const closeChat = document.getElementById("closeChat");
  const chatMessages = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const sendButton = document.getElementById("sendMessage");

  // Debug logging
  console.log("Chat elements:", {
    chatButton: !!chatButton,
    chatExpandable: !!chatExpandable,
    chatInput: !!chatInput,
    sendButton: !!sendButton,
  });

  if (chatButton && chatExpandable) {
    chatButton.addEventListener("click", function () {
      chatExpandable.classList.toggle("show");
      // Force visibility check after opening
      setTimeout(() => {
        const inputSection = document.querySelector(".chat-input");
        if (inputSection) {
          console.log("Input section found:", inputSection);
          inputSection.style.display = "flex";
          inputSection.style.visibility = "visible";
        }
      }, 100);
    });
  }

  if (closeChat) {
    closeChat.addEventListener("click", function () {
      chatExpandable.classList.remove("show");
    });
  }

  if (sendButton && chatInput) {
    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  }
}

async function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const chatMessages = document.getElementById("chatMessages");
  const sendButton = document.getElementById("sendMessage");
  const message = chatInput.value.trim();

  if (message) {
    // Add user message
    addMessage(message, "user");
    chatInput.value = "";

    // Disable send button and show loading state
    sendButton.disabled = true;
    sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    // Add typing indicator
    addTypingIndicator();

    try {
      // Call the API endpoint through our proxy
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: message,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Remove typing indicator
      removeTypingIndicator();

      // Add bot response
      addMessage(data.answer, "bot");
    } catch (error) {
      console.error("Error calling chat API:", error);

      // Remove typing indicator
      removeTypingIndicator();

      // Add error message
      addMessage(
        "I'm sorry, I'm having trouble connecting right now. Please try again later.",
        "bot"
      );
    } finally {
      // Re-enable send button
      sendButton.disabled = false;
      sendButton.innerHTML =
        '<i class="fas fa-paper-plane"></i><span class="sr-only">Send</span>';
    }
  }
}

function addMessage(content, sender) {
  const chatMessages = document.getElementById("chatMessages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.textContent = content;

  messageDiv.appendChild(contentDiv);
  chatMessages.appendChild(messageDiv);

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
  const chatMessages = document.getElementById("chatMessages");
  const typingDiv = document.createElement("div");
  typingDiv.className = "message bot-message typing-indicator";
  typingDiv.id = "typing-indicator";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.innerHTML =
    '<div class="typing-dots"><span></span><span></span><span></span></div>';

  typingDiv.appendChild(contentDiv);
  chatMessages.appendChild(typingDiv);

  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
  const typingIndicator = document.getElementById("typing-indicator");
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Smooth scrolling
function initializeSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Animation on scroll
function initializeAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fade-in");
      }
    });
  }, observerOptions);

  // Observe cards and sections
  document.querySelectorAll(".card, .stat-item, section").forEach((el) => {
    observer.observe(el);
  });
}

// Form enhancements
function initializeFormEnhancements() {
  // Add loading states to forms
  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", function () {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML =
          '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        submitBtn.disabled = true;
      }
    });
  });

  // Character counter for textareas
  document.querySelectorAll("textarea").forEach((textarea) => {
    const maxLength = textarea.getAttribute("maxlength");
    if (maxLength) {
      const counter = document.createElement("small");
      counter.className = "form-text text-muted";
      counter.textContent = `0/${maxLength} characters`;

      textarea.parentNode.appendChild(counter);

      textarea.addEventListener("input", function () {
        const remaining = maxLength - this.value.length;
        counter.textContent = `${this.value.length}/${maxLength} characters`;
        counter.className = `form-text ${
          remaining < 50 ? "text-danger" : "text-muted"
        }`;
      });
    }
  });
}

// Utility functions
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  notification.style.cssText =
    "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  document.body.appendChild(notification);

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, 5000);
}

// Search functionality
function initializeSearch() {
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const query = this.value.toLowerCase();
      const items = document.querySelectorAll(".project-item, .blog-item");

      items.forEach((item) => {
        const text = item.textContent.toLowerCase();
        if (text.includes(query)) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  }
}

// Image lazy loading
function initializeLazyLoading() {
  const images = document.querySelectorAll("img[data-src]");

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.classList.remove("lazy");
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach((img) => imageObserver.observe(img));
}

// Back to top button
function initializeBackToTop() {
  const backToTop = document.createElement("button");
  backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
  backToTop.className = "btn btn-primary position-fixed";
  backToTop.style.cssText =
    "bottom: 100px; right: 30px; z-index: 999; display: none; border-radius: 50%; width: 50px; height: 50px;";
  backToTop.setAttribute("aria-label", "Back to top");

  document.body.appendChild(backToTop);

  window.addEventListener("scroll", function () {
    if (window.pageYOffset > 300) {
      backToTop.style.display = "block";
    } else {
      backToTop.style.display = "none";
    }
  });

  backToTop.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}

// Initialize all features
document.addEventListener("DOMContentLoaded", function () {
  initializeSearch();
  initializeLazyLoading();
  initializeBackToTop();
});
