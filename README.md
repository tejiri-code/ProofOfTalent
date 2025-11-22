# ProofOfTalent AI

An AI-powered assessment platform for the UK Global Talent Visa application process. Get a detailed, personalized roadmap for your visa application in minutes.

## 🎯 Overview

ProofOfTalent AI helps professionals assess their eligibility for the UK Global Talent Visa by analyzing their profile against the official endorsing body criteria. The system provides:

- **Instant Assessment**: AI-powered analysis of your qualifications and experience
- **Personalized Roadmap**: Step-by-step guidance tailored to your profile
- **Evidence Recommendations**: Specific suggestions for strengthening your application
- **Eligibility Scoring**: Clear breakdown of how you match visa requirements

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- React components with Geist font system

**Backend:**
- Python FastAPI (assumed based on typical AI system architecture)
- AI/ML models for visa eligibility assessment
- Database for user profiles and assessments

### Project Structure

```
ProofOfTalent/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout with header
│   │   │   ├── page.tsx         # Landing page
│   │   │   └── globals.css      # Global styles
│   │   └── components/
│   │       └── Logo.tsx         # Brand logo component
│   ├── public/                  # Static assets
│   └── package.json
├── backend/                     # API and ML services
└── README.md
```

## 🚀 Features

### 1. Profile Analysis
- Upload CV/resume or fill in profile form
- Automatic extraction of relevant experience
- Skills and achievements parsing

### 2. Eligibility Assessment
- Comparison against Tech Nation, Royal Society, or Arts Council criteria
- Scoring based on:
  - Technical expertise
  - Innovation and impact
  - Recognition and awards
  - Publications and contributions
  - Leadership and influence

### 3. Personalized Roadmap
- Gap analysis showing what's missing
- Actionable steps to strengthen application
- Timeline recommendations
- Evidence collection checklist

### 4. Document Recommendations
- Suggested reference letters
- Evidence documentation templates
- Portfolio organization tips

## 🛠️ Setup Instructions

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ (for backend)
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

### Environment Variables

Create `.env.local` in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Proof of Talent
```

Create `.env` in the backend directory:

```env
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

## 📖 Usage

1. **Landing Page**: Overview of the service and how it works
2. **Profile Input**: Enter your professional information
3. **AI Assessment**: System analyzes your profile (1-2 minutes)
4. **Results Dashboard**: View your eligibility score and recommendations
5. **Roadmap**: Follow personalized steps to improve your application

## 🔒 Data Privacy

- All user data is encrypted at rest and in transit
- GDPR compliant data handling
- Users can request data deletion at any time
- No data sharing with third parties

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm test
npm run test:e2e

# Backend tests
cd backend
pytest
```

## 📦 Deployment

### Frontend (Vercel)

```bash
vercel --prod
```

### Backend (Docker)

```bash
docker build -t proofoftalent-api .
docker run -p 8000:8000 proofoftalent-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For questions or support:

- Issues: GitHub Issues tab

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Mobile app (iOS/Android)
- [ ] Integration with LinkedIn profiles
- [ ] Community forum for applicants
- [ ] Success story database
- [ ] Immigration lawyer marketplace

## ⚖️ Legal Disclaimer

ProofOfTalent AI provides guidance and recommendations based on publicly available information about the UK Global Talent Visa. This is not legal advice. Always consult with a qualified immigration lawyer for official guidance.

## 🙏 Acknowledgments

- UK Government immigration guidelines
- Tech Nation, Royal Society, and Arts Council criteria
- Community feedback and success stories

---

Built with ❤️ for global talent seeking opportunities in the UK
