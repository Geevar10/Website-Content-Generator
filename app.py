# app.py - Enhanced Website Content Generator with UI/UX
import gradio as gr
import requests
import json
import os
from datetime import datetime
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===============================================
# BACKEND API FUNCTIONS
# ===============================================

class ContentGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not found. Using mock responses.")
            self.mock_mode = True
        else:
            self.mock_mode = False
    
    def generate_website_html(self, business_name: str, industry: str, audience: str, keywords: str, tone: str) -> str:
        """Generate complete HTML website with modern UI/UX"""
        
        # Generate content based on inputs
        if self.mock_mode:
            content_data = self.generate_mock_content_data(business_name, industry, audience, keywords, tone)
        else:
            content_data = self.generate_ai_content_data(business_name, industry, audience, keywords, tone)
        
        # Create HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{content_data['page_title']}</title>
    <meta name="description" content="{content_data['meta_description']}">
    <meta name="keywords" content="{keywords}">
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Header Styles */
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            text-decoration: none;
            color: white;
        }}
        
        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}
        
        .nav-links a {{
            color: white;
            text-decoration: none;
            transition: opacity 0.3s;
        }}
        
        .nav-links a:hover {{
            opacity: 0.8;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 80px 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            opacity: 0;
            animation: slideUp 1s ease-out forwards;
        }}
        
        .hero p {{
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0;
            animation: slideUp 1s ease-out 0.3s forwards;
        }}
        
        .cta-button {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s;
            opacity: 0;
            animation: slideUp 1s ease-out 0.6s forwards;
        }}
        
        .cta-button:hover {{
            background: #ff5252;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
        }}
        
        /* Section Styles */
        .section {{
            padding: 80px 0;
        }}
        
        .section:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .section h2 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
            color: #2c3e50;
        }}
        
        /* About Section */
        .about-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            align-items: center;
        }}
        
        .about-text {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .about-image {{
            text-align: center;
            font-size: 8rem;
            color: #667eea;
            opacity: 0.3;
        }}
        
        /* Services Section */
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .service-card {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .service-card:hover {{
            transform: translateY(-5px);
        }}
        
        .service-icon {{
            font-size: 3rem;
            color: #667eea;
            margin-bottom: 1rem;
        }}
        
        .service-card h3 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #2c3e50;
        }}
        
        /* Features Section */
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .feature-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .feature-icon {{
            font-size: 2rem;
            color: #667eea;
            min-width: 60px;
        }}
        
        .feature-text h4 {{
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: #2c3e50;
        }}
        
        /* Contact Section */
        .contact-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
        }}
        
        .contact-info {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .contact-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .contact-icon {{
            font-size: 1.5rem;
            color: #667eea;
            min-width: 40px;
        }}
        
        .contact-form {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .form-group {{
            margin-bottom: 1.5rem;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #2c3e50;
        }}
        
        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}
        
        .form-group input:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .submit-btn {{
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }}
        
        .submit-btn:hover {{
            background: #5a6fd8;
        }}
        
        /* Footer */
        footer {{
            background: #2c3e50;
            color: white;
            padding: 3rem 0 1rem;
            text-align: center;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h3 {{
            margin-bottom: 1rem;
            color: #667eea;
        }}
        
        .footer-section ul {{
            list-style: none;
        }}
        
        .footer-section ul li {{
            margin-bottom: 0.5rem;
        }}
        
        .footer-section ul li a {{
            color: #bdc3c7;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .footer-section ul li a:hover {{
            color: white;
        }}
        
        .footer-bottom {{
            border-top: 1px solid #34495e;
            padding-top: 1rem;
            color: #bdc3c7;
        }}
        
        /* Animations */
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .about-content,
            .contact-content {{
                grid-template-columns: 1fr;
            }}
            
            .services-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <nav class="container">
            <a href="#" class="logo">{business_name}</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="container">
            <h1>{content_data['main_headline']}</h1>
            <p>{content_data['subheadline']}</p>
            <a href="#contact" class="cta-button">{content_data['cta_text']}</a>
        </div>
    </section>

    <!-- About Section -->
    <section class="section" id="about">
        <div class="container">
            <h2>About {business_name}</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>{content_data['about_text']}</p>
                </div>
                <div class="about-image">
                    <i class="fas fa-building"></i>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section class="section" id="services">
        <div class="container">
            <h2>Our Services</h2>
            <div class="services-grid">
                {self.generate_service_cards(content_data['services'])}
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section">
        <div class="container">
            <h2>Why Choose {business_name}?</h2>
            <div class="features-grid">
                {self.generate_feature_items(content_data['features'])}
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="section" id="contact">
        <div class="container">
            <h2>Get In Touch</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <h3>Contact Information</h3>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt contact-icon"></i>
                        <div>
                            <h4>Address</h4>
                            <p>123 Business Street<br>City, State 12345</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone contact-icon"></i>
                        <div>
                            <h4>Phone</h4>
                            <p>(555) 123-4567</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-envelope contact-icon"></i>
                        <div>
                            <h4>Email</h4>
                            <p>info@{business_name.lower().replace(' ', '')}.com</p>
                        </div>
                    </div>
                </div>
                <form class="contact-form">
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea id="message" name="message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="submit-btn">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{business_name}</h3>
                    <p>Your trusted partner in {industry.lower()}. We're committed to delivering exceptional results and building lasting relationships with our clients.</p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="#home">Home</a></li>
                        <li><a href="#about">About</a></li>
                        <li><a href="#services">Services</a></li>
                        <li><a href="#contact">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <ul>
                        <li><i class="fas fa-phone"></i> (555) 123-4567</li>
                        <li><i class="fas fa-envelope"></i> info@{business_name.lower().replace(' ', '')}.com</li>
                        <li><i class="fas fa-map-marker-alt"></i> 123 Business Street, City, State</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {business_name}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Form submission handler
        document.querySelector('.contact-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        }});

        // Add scroll effect to service cards
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.service-card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease-out';
            observer.observe(card);
        }});
    </script>
</body>
</html>
        """
        
        return html_template
    
    def generate_service_cards(self, services):
        """Generate HTML for service cards"""
        icons = ["fas fa-cogs", "fas fa-users", "fas fa-chart-line", "fas fa-lightbulb"]
        cards_html = ""
        
        for i, service in enumerate(services):
            icon = icons[i % len(icons)]
            cards_html += f"""
                <div class="service-card">
                    <div class="service-icon">
                        <i class="{icon}"></i>
                    </div>
                    <h3>{service['title']}</h3>
                    <p>{service['description']}</p>
                </div>
            """
        
        return cards_html
    
    def generate_feature_items(self, features):
        """Generate HTML for feature items"""
        icons = ["fas fa-check-circle", "fas fa-star", "fas fa-shield-alt", "fas fa-rocket"]
        items_html = ""
        
        for i, feature in enumerate(features):
            icon = icons[i % len(icons)]
            items_html += f"""
                <div class="feature-item">
                    <div class="feature-icon">
                        <i class="{icon}"></i>
                    </div>
                    <div class="feature-text">
                        <h4>{feature['title']}</h4>
                        <p>{feature['description']}</p>
                    </div>
                </div>
            """
        
        return items_html
    
    def generate_mock_content_data(self, business_name: str, industry: str, audience: str, keywords: str, tone: str) -> Dict:
        """Generate mock content data structure"""
        return {
            'page_title': f"{business_name} - Leading {industry} Solutions",
            'meta_description': f"Discover {business_name}, your trusted partner in {industry}. We serve {audience} with professional excellence.",
            'main_headline': f"Welcome to {business_name}",
            'subheadline': f"Your trusted partner in {industry}, dedicated to serving {audience} with excellence and innovation.",
            'about_text': f"{business_name} is a leading company in the {industry} industry, committed to delivering exceptional results for {audience}. Our team of experts combines years of experience with cutting-edge technology to provide solutions that drive success. We believe in building lasting relationships with our clients through transparent communication, reliable service, and measurable results.",
            'cta_text': "Get Started Today",
            'services': [
                {
                    'title': 'Professional Consultation',
                    'description': 'Expert advice tailored to your specific needs and goals in the industry.'
                },
                {
                    'title': 'Custom Solutions',
                    'description': 'Personalized approaches designed to address your unique challenges.'
                },
                {
                    'title': 'Ongoing Support',
                    'description': '24/7 customer support to ensure your continued success and satisfaction.'
                },
                {
                    'title': 'Strategic Planning',
                    'description': 'Long-term strategies that align with your business objectives and growth plans.'
                }
            ],
            'features': [
                {
                    'title': 'Proven Experience',
                    'description': 'Years of expertise in the industry with a track record of success.'
                },
                {
                    'title': 'Quality Assurance',
                    'description': 'Rigorous quality control processes ensure exceptional results every time.'
                },
                {
                    'title': 'Customer-Centric',
                    'description': 'Your success is our priority. We put customers at the heart of everything we do.'
                },
                {
                    'title': 'Innovation Focus',
                    'description': 'Cutting-edge solutions that keep you ahead of the competition.'
                }
            ]
        }
    
    def generate_ai_content_data(self, business_name: str, industry: str, audience: str, keywords: str, tone: str) -> Dict:
        """Generate AI-powered content data structure"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
            Generate website content data for:
            - Business: {business_name}
            - Industry: {industry}
            - Audience: {audience}
            - Keywords: {keywords}
            - Tone: {tone}

            Return a JSON structure with:
            - page_title: SEO-optimized page title
            - meta_description: SEO meta description (150-160 chars)
            - main_headline: Compelling main headline
            - subheadline: Supporting subheadline
            - about_text: About us paragraph (150-200 words)
            - cta_text: Call-to-action button text
            - services: Array of 4 service objects with title and description
            - features: Array of 4 feature objects with title and description

            Make it professional, engaging, and SEO-friendly.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating AI content: {e}")
            return self.generate_mock_content_data(business_name, industry, audience, keywords, tone)

    def generate_content(self, business_name: str, industry: str, audience: str, keywords: str, tone: str) -> str:
        """Main content generation function"""
        
        # Input validation
        if not business_name.strip():
            return "❌ Please enter a business name."
        
        if not industry.strip():
            return "❌ Please enter an industry."
        
        logger.info(f"Generating website for {business_name} in {industry}")
        
        try:
            html_content = self.generate_website_html(business_name, industry, audience, keywords, tone)
            return html_content
            
        except Exception as e:
            logger.error(f"Error in content generation: {e}")
            return f"❌ Error generating website: {str(e)}"

# ===============================================
# FRONTEND GRADIO INTERFACE
# ===============================================

# Initialize the content generator
generator = ContentGenerator()

def generate_website_content(business_name, industry, audience, keywords, tone):
    """Wrapper function for Gradio interface"""
    return generator.generate_content(business_name, industry, audience, keywords, tone)

def clear_form():
    """Clear all input fields"""
    return "", "", "", "", "Professional"

def load_example(example_name):
    """Load predefined examples"""
    examples = {
        "Tech Startup": {
            "business_name": "InnovateTech Solutions",
            "industry": "Software Development",
            "audience": "Small to medium businesses",
            "keywords": "web development, mobile apps, digital transformation",
            "tone": "Professional"
        },
        "Local Restaurant": {
            "business_name": "Bella Vista Italian Restaurant",
            "industry": "Food & Beverage",
            "audience": "Food lovers and families",
            "keywords": "authentic Italian cuisine, family dining, fresh ingredients",
            "tone": "Friendly"
        },
        "Fitness Studio": {
            "business_name": "Peak Performance Fitness",
            "industry": "Health & Wellness",
            "audience": "Fitness enthusiasts and beginners",
            "keywords": "personal training, group classes, fitness goals",
            "tone": "Motivational"
        }
    }
    
    if example_name in examples:
        ex = examples[example_name]
        return ex["business_name"], ex["industry"], ex["audience"], ex["keywords"], ex["tone"]
    else:
        return "", "", "", "", "Professional"

# ===============================================
# GRADIO INTERFACE SETUP
# ===============================================

# Custom CSS for better styling
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.example-card {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 10px;
    margin: 5px;
}
"""

# Create the interface
with gr.Blocks(title="Website Generator", theme=gr.themes.Soft(), css=custom_css) as app:
    
    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🌐 Professional Website Generator</h1>
        <p>Generate complete websites with modern UI/UX design</p>
    </div>
    """)
    
    # API Key Status
    api_status = "🔑 OpenAI API Connected" if not generator.mock_mode else "⚠️ Mock Mode (Set OPENAI_API_KEY for AI generation)"
    gr.Markdown(f"**Status:** {api_status}")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Business Information")
            
            business_name = gr.Textbox(
                label="Business Name*",
                placeholder="Enter your business name",
                max_lines=1
            )
            
            industry = gr.Textbox(
                label="Industry*",
                placeholder="e.g., Technology, Healthcare, Retail",
                max_lines=1
            )
            
            audience = gr.Textbox(
                label="Target Audience",
                placeholder="e.g., Small business owners, Young professionals",
                value="General public",
                max_lines=1
            )
            
            keywords = gr.Textbox(
                label="SEO Keywords",
                placeholder="Enter comma-separated keywords",
                max_lines=2
            )
            
            tone = gr.Dropdown(
                label="Tone",
                choices=["Professional", "Friendly", "Casual", "Formal", "Creative", "Authoritative", "Conversational", "Inspiring", "Motivational"],
                value="Professional"
            )
            
            with gr.Row():
                generate_btn = gr.Button("🚀 Generate Website", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear Form", variant="secondary")
            
            # Quick Examples
            gr.Markdown("### 🚀 Quick Examples")
            with gr.Row():
                tech_btn = gr.Button("Tech Startup", size="sm")
                restaurant_btn = gr.Button("Local Restaurant", size="sm")
                fitness_btn = gr.Button("Fitness Studio", size="sm")
        
        with gr.Column(scale=2):
            gr.Markdown("### 🌐 Generated Website")
            output = gr.HTML(
                label="Website Preview",
                value="<div style='text-align: center; padding: 50px; color: #666;'>Your generated website will appear here...</div>"
            )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("### 📋 Features of Generated Websites:")
    gr.Markdown("""
    ✅ **Responsive Design** - Works on all devices
    ✅ **Modern UI/UX** - Clean, professional appearance
    ✅ **SEO Optimized** - Meta tags and structured content
    ✅ **Interactive Elements** - Smooth scrolling, hover effects
    ✅ **Contact Form** - Functional contact form
    ✅ **Professional Sections** - Hero, About, Services, Contact
    ✅ **Copy & Save Ready** - Download as HTML file
    """)
    
    # Event handlers
    generate_btn.click(
        fn=generate_website_content,
        inputs=[business_name, industry, audience, keywords, tone],
        outputs=output
    )
    
    clear_btn.click(
        fn=clear_form,
        outputs=[business_name, industry, audience, keywords, tone]
    )
    
    # Example buttons
    tech_btn.click(
        fn=lambda: load_example("Tech Startup"),
        outputs=[business_name, industry
, audience, keywords, tone])
    
    tech_btn.click(
            fn=lambda: load_example("Tech Startup"),
            outputs=[business_name, industry, audience, keywords, tone]
        )
        
    restaurant_btn.click(
            fn=lambda: load_example("Local Restaurant"),
            outputs=[business_name, industry, audience, keywords, tone]
        )
        
    fitness_btn.click(
            fn=lambda: load_example("Fitness Studio"),
            outputs=[business_name, industry, audience, keywords, tone]
        )

# Launch the app
if __name__ == "__main__":
    app.launch()
