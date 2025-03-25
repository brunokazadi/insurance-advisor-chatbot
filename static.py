# ----------------------------------------------------------------------------- 
# JavaScript Animations & Theme Toggle 
# -----------------------------------------------------------------------------

JS_ANIMATE = """
function load_animate() {
  // Create a container for both the icon and the header text
  var container = document.createElement('div');
  container.id = 'gradio-animation';
  container.style.display = 'flex';
  container.style.flexDirection = 'column';
  container.style.alignItems = 'center';
  container.style.justifyContent = 'center';
  container.style.textAlign = 'center';
  container.style.padding = '20px';
  container.style.transform = "translateY(-50px)";
  container.style.opacity = "0";
  container.style.transition = "transform 1s ease-out, opacity 1s ease-out";
  
  // Create image element for the insurance icon
  var icon = document.createElement('img');
  icon.src = "https://github.com/brunokazadi/insurance-advisor-chatbot/blob/main/insurance-icon.png?raw=true";
  icon.style.width = "150px";
  icon.style.height = "150px";
  icon.style.marginBottom = "20px"; // Spacing between icon and text
  container.appendChild(icon);
  
  // Create text element for the header text
  var textContainer = document.createElement('div');
  textContainer.style.fontSize = '36pt';
  textContainer.style.fontWeight = 'bold';
  
  var text = "Welcome to InsureBot, your trusted insurance advisor!";
  var specialWord = "InsureBot";
  var specialColor = "#91CFE5";
  let delay = 0;
  // Create letter-by-letter spans with individual transition delays
  for (let i = 0; i < text.length; i++) {
      let span = document.createElement('span');
      span.innerText = text[i];
      span.style.opacity = "0";
      span.style.transition = "opacity 0.5s ease " + (delay * 50) + "ms";
      if (text.substring(i, i + specialWord.length) === specialWord) {
          span.style.color = specialColor;
      }
      textContainer.appendChild(span);
      delay++;
  }
  container.appendChild(textContainer);
  
  // Insert the container at the top of the gradio container
  var gradioContainer = document.querySelector('.gradio-container');
  gradioContainer.insertBefore(container, gradioContainer.firstChild);
  
  // Trigger container's slide-in and fade-in
  setTimeout(function() {
      container.style.transform = "translateY(0)";
      container.style.opacity = "1";
  }, 100);
  
  // Trigger letter fade-in for the text element
  var spans = textContainer.getElementsByTagName('span');
  for (let i = 0; i < spans.length; i++) {
      (function(index) {
          setTimeout(function() {
              spans[index].style.opacity = "1";
          }, 100);
      })(i);
  }
  
  // Set default theme to light mode
  var gradioContainerElement = document.querySelector(".gradio-container");
  if (gradioContainerElement) {
      gradioContainerElement.classList.add("light-mode");
  }
}
"""

JS_THEME = """
function toggleTheme() {
    var theme = localStorage.getItem("theme");
    // Default to light mode when theme is not set
    var isDarkMode = (theme === "dark");
    var gradioContainer = document.querySelector(".gradio-container");
    var targetedSpans = Array.from(document.querySelectorAll("span")).filter(function(span) {
        return span.innerText === "Enable Text-to-Speech" || span.innerText === "Activer la Synthèse Vocale";
    });
    
    if (isDarkMode) {
        gradioContainer.classList.remove("dark-mode");
        document.body.classList.remove("dark-mode");
        gradioContainer.classList.add("light-mode");
        document.body.classList.add("light-mode");
        targetedSpans.forEach(function(span) {
            span.classList.remove("dark-mode");
            span.classList.add("light-mode");
        });
        localStorage.setItem("theme", "light");
        document.getElementById("theme-toggle-btn").innerHTML = "☼";
        
        // Reset all dropdown styles when switching back to light mode
        document.querySelectorAll('select, option, [role="listbox"], [role="option"], [role="combobox"], .gradio-dropdown, [data-testid="dropdown"], div[class*="svelte"], div[class*="gradio-dropdown"]').forEach(function(el) {
            el.style.backgroundColor = "";
            el.style.color = "";
            el.style.borderColor = "";
            
            // Clear styles on all children too
            el.querySelectorAll('*').forEach(function(child) {
                child.style.backgroundColor = "";
                child.style.color = "";
                child.style.borderColor = "";
            });
        });
        
        // Force reset all dropdowns regardless of their class or attributes
        setTimeout(function() {
            var allElements = document.querySelectorAll('*');
            for (var i = 0; i < allElements.length; i++) {
                var el = allElements[i];
                if (el.tagName === 'SELECT' || 
                    (el.tagName === 'DIV' && el.getAttribute('role') === 'listbox') ||
                    el.classList.contains('gradio-dropdown') ||
                    el.hasAttribute('data-testid') && el.getAttribute('data-testid') === 'dropdown') {
                    el.style.backgroundColor = "";
                    el.style.color = "";
                    
                    // Also reset all children
                    var children = el.querySelectorAll('*');
                    for (var j = 0; j < children.length; j++) {
                        children[j].style.backgroundColor = "";
                        children[j].style.color = "";
                    }
                }
            }
        }, 50);
    } else {
        gradioContainer.classList.remove("light-mode");
        document.body.classList.remove("light-mode");
        gradioContainer.classList.add("dark-mode");
        document.body.classList.add("dark-mode");
        targetedSpans.forEach(function(span) {
            span.classList.remove("light-mode");
            span.classList.add("dark-mode");
        });
        localStorage.setItem("theme", "dark");
        document.getElementById("theme-toggle-btn").innerHTML = "☾";
        
        // Apply dark styles to dropdowns
        setTimeout(function() {
            document.querySelectorAll('select, option, [role="listbox"], [role="option"], [role="combobox"], .gradio-dropdown, [data-testid="dropdown"], div[class*="svelte"], div[class*="gradio-dropdown"]').forEach(function(el) {
                el.style.backgroundColor = "#1f1f1f";
                el.style.color = "#ffffff";
                el.style.borderColor = "#444";
                
                // Apply to all children as well
                el.querySelectorAll('*').forEach(function(child) {
                    child.style.backgroundColor = "#1f1f1f";
                    child.style.color = "#ffffff";
                });
            });
            
            // Specifically target the language dropdown
            const langDropdown = document.querySelector('#language-dropdown') || 
                Array.from(document.querySelectorAll('div')).find(function(el) {
                    return el.innerText && (el.innerText.includes('English') || el.innerText.includes('Français')) && 
                    el.getBoundingClientRect().top < 200;
                });
            
            if (langDropdown) {
                langDropdown.style.backgroundColor = "#1f1f1f";
                langDropdown.style.color = "#ffffff";
                const allChildren = langDropdown.querySelectorAll('*');
                allChildren.forEach(function(child) {
                    child.style.backgroundColor = "#1f1f1f";
                    child.style.color = "#ffffff";
                });
            }
        }, 100);
    }
}
"""

# ----------------------------------------------------------------------------- 
# CSS Styles 
# -----------------------------------------------------------------------------

STYLE = """
<style>
  #gradio-animation {
    margin: 40px 0;
  }
  #send-button {
    width: 20%;
    align-self: end;
    margin-left: auto;
  }
  #theme-toggle-btn {
    min-width: 5%;
    align-self: end;
    margin-left: auto;
  }
  #language-container {
    display: flex;
    justify-content: flex-start;
    width: 20%;
    align-items: flex-end;
    align-self: end;
  }
  #language-dropdown {
    width: 20%;
    position: relative;
    margin: 0;
  }
  #checkbox {
    width: 5%;
    align-self: end;
    margin-left: auto;
  }
  h1 { text-align:center; font-size: 24px; margin-bottom: 10px; }
  .subtitle { text-align:center; font-size: 18px; margin-bottom: 20px; }
  .light-mode, .dark-mode {
    transition: background-color 0.3s ease !important;
  }
  .light-mode {
    background-color: #ededed !important;
    color: #000000 !important;
  }
  .dark-mode {
    background-color: #0f0f11 !important;
    color: #ffffff !important;
  }
  .light-mode h1, .light-mode h3, .light-mode p, 
  .light-mode li, .light-mode strong, .light-mode .svelte-i3tvor,
  .light-mode .svelte-p5q82i {
    color: #000 !important;
  }
  .dark-mode h1, .dark-mode h3, .dark-mode p, 
  .dark-mode li, .dark-mode strong, .dark-mode .svelte-i3tvor,
  .dark-mode .svelte-p5q82i {
    color: #ffffff !important;
  }
  .light-mode .bubble-wrap, 
  .light-mode .multimodal-textbox, .light-mode .svelte-i3tvor {
    background-color: #ffffff !important;
  }
  .dark-mode .bubble-wrap, 
  .dark-mode .multimodal-textbox, .dark-mode .svelte-i3tvor  {
    background-color: #201c1c !important;
  }
  .light-mode .bot, .light-mode .message, .light-mode .placeholder-content,
  .light-mode .progress-text {
    background-color: rgb(245, 245, 245) !important;
    border-color: rgb(185, 182, 182) !important;
  }
  .dark-mode .bot, .dark-mode .message, .dark-mode .placeholder-content,
  .dark-mode .progress-text {
    background-color: #27272a !important;
    border-color: #3f3f46 !important;
  }
  .light-mode textarea, .light-mode .gradio-slider input, 
  .light-mode gradio-textbox, .light-mode #language-dropdown textarea {
    background-color: #ededed !important;
    color: #000 !important;
    border: 1px solid rgb(185, 182, 182) !important;
  }
  .dark-mode textarea, .dark-mode .gradio-slider input, 
  .dark-mode gradio-textbox, .dark-mode #language-dropdown textarea {
    background-color: #27272a !important;
    color: #ffffff !important;
    border: 1px solid #444 !important;
  }
  .light-mode button {
    background-color: #d1d1d1 !important;
    color: #000 !important;
    border: 1px solid #ccc !important;
  }
  .dark-mode button {
    background-color: #282828 !important;
    color: #fff !important;
    border: 1px solid #444 !important;
  }
  .light-mode button:hover {
    background-color: #bbb !important;
    transition: background-color 0.3s ease !important;
  }
  .dark-mode button:hover {
    background-color: #151515 !important;
    transition: background-color 0.3s ease !important;
  }
  .light-mode .gr-markdown,
  .light-mode .gradio-container .gr-markdown {
      color: #000 !important;
  }
  .dark-mode .gr-markdown,
  .dark-mode .gradio-container .gr-markdown {
      color: #ffffff !important;
  }
  
  /* Button style */
  .example-btn {
    margin: 5px;
    padding: 10px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
  }
  .example-btn:hover {
    background-color: #e0e0e0;
  }
  .examples-container {
    margin-top: 10px;
    padding: 10px;
    border-radius: 4px;
  }
  .examples-header {
    font-weight: bold;
    margin-bottom: 10px;
  }
  .lang-examples {
    width: 100%;
  }
  
  /* File upload indicator */
  .file-info {
    background-color: #f8f9fa;
    border-left: 3px solid #007bff;
    padding: 8px 12px;
    margin: 10px 0;
    font-size: 14px;
    border-radius: 0 4px 4px 0;
  }
  .light-mode .file-info {
    background-color: #f0f0f0;
    color: #333;
  }
  .dark-mode .file-info {
    background-color: #333;
    color: #f0f0f0;
    border-left: 3px solid #4da6ff;
  }
  
  /* Dropdown styling fixes for dark mode - Aggressive approach */
  /* These are "!important" to override any Gradio styles */
  .dark-mode select,
  .dark-mode option,
  .dark-mode [role="listbox"],
  .dark-mode [role="option"],
  .dark-mode [role="combobox"],
  .dark-mode .gradio-dropdown,
  .dark-mode [data-testid="dropdown"],
  .dark-mode div[class*="svelte"],
  .dark-mode div[class*="gradio-dropdown"] {
    background-color: #1f1f1f !important;
    color: #ffffff !important;
    border-color: #444 !important;
  }
  
  /* Fix specifically for language dropdown */
  body.dark-mode #language-dropdown > *,
  .dark-mode #language-dropdown > *,
  .dark-mode #language-dropdown select,
  .dark-mode #language-dropdown [data-testid="dropdown"],
  .dark-mode #language-dropdown [data-testid="dropdown"] * {
    background-color: #1f1f1f !important;
    color: #ffffff !important;
  }
  
  /* Important inline element override */
  .dark-mode select,
  .dark-mode select * {
    background-color: #1f1f1f !important;
    color: white !important;
  }
  
  /* Light mode specific overrides to ensure dropdowns reset properly */
  .light-mode select,
  .light-mode option,
  .light-mode [role="listbox"],
  .light-mode [role="option"],
  .light-mode [role="combobox"],
  .light-mode .gradio-dropdown,
  .light-mode [data-testid="dropdown"] {
    background-color: #ffffff !important;
    color: #000000 !important;
  }
</style>
"""

# Additional script to reset styles in light mode
THEME_RESET_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Create a function to reset all dropdown styles when in light mode
    function resetLightModeStyles() {
        if (!document.body.classList.contains('dark-mode') && document.body.classList.contains('light-mode')) {
            // Select all potentially styled elements
            const elements = document.querySelectorAll('select, option, [role="listbox"], [role="option"], [role="combobox"], .gradio-dropdown, [data-testid="dropdown"]');
            
            // Reset their styles
            elements.forEach(function(el) {
                el.style.backgroundColor = "#ffffff";
                el.style.color = "#000000";
                
                // Reset their children
                const children = el.querySelectorAll('*');
                children.forEach(function(child) {
                    child.style.backgroundColor = "#ffffff";
                    child.style.color = "#000000";
                });
            });
        }
    }
    
    // Run when document loads
    setTimeout(resetLightModeStyles, 500);
    
    // Set up an observer to watch for theme changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                if (document.body.classList.contains('light-mode')) {
                    setTimeout(resetLightModeStyles, 100);
                    setTimeout(resetLightModeStyles, 500); // Run again after a delay to catch elements that might load later
                }
            }
        });
    });
    
    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
    });
    
    // Also run periodically to catch any new elements
    setInterval(function() {
        if (document.body.classList.contains('light-mode')) {
            resetLightModeStyles();
        }
    }, 2000);
});
</script>
"""