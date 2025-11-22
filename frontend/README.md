# UK Global Talent Visa Analysis - Frontend

Next.js frontend for the UK Global Talent visa analysis system.

## Features

- **Multi-step Wizard**: Guided flow through field selection, questionnaire, document upload, and results
- **Field Selection**: Choose from Digital Technology, Arts & Culture, or Science & Research
- **Dynamic Questionnaire**: Field-specific questions
- **Document Upload**: Upload CV, recommendation letters, and portfolio items
- **Real-time Analysis**: LLM-powered analysis with GPT-4
- **Visual Results**: Beautiful visualization of likelihood score, strengths, gaps, and roadmap

## Tech Stack

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS 4
- API Integration with FastAPI backend

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
# Edit .env.local if backend is not at localhost:8000
```

3. Run development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── page.tsx          # Main application with wizard flow
│   ├── components/
│   │   ├── FieldSelection.tsx       # Step 1: Field selection
│   │   ├── QuestionnaireStep.tsx    # Step 2: Questionnaire
│   │   ├── DocumentUpload.tsx       # Step 3: Document upload
│   │   └── AnalysisResults.tsx      # Step 4: Results display
│   └── lib/
│       └── api.ts            # API client for backend
├── public/                    # Static assets
└── package.json
```

## Usage Flow

1. **Select Field**: Choose your field of expertise
2. **Answer Questionnaire**: Fill out field-specific questions
3. **Upload Documents**: Upload CV and supporting documents
4. **View Results**: See likelihood score, strengths, gaps, and personalized roadmap

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

## API Integration

The frontend communicates with the backend API at the URL specified in `NEXT_PUBLIC_API_URL`. Make sure the backend is running before starting the frontend.

Backend should be running at `http://localhost:8000` (see backend/README.md)

## Components

### FieldSelection
First step where user selects their field (Digital Technology, Arts & Culture, or Science & Research).

### QuestionnaireStep
Dynamic questionnaire based on selected field. Questions include years of experience, publications, awards, etc.

### DocumentUpload
Multi-file upload interface for PDF documents (CV, recommendation letters, portfolio items).

### AnalysisResults
Results display showing:
- Likelihood percentage with visual progress ring
- Assessment level (Exceptional Talent / Exceptional Promise)
- Strengths list
- Gaps with severity indicators
- Personalized roadmap with milestones

## Styling

Uses Tailwind CSS for styling with a modern, clean design featuring:
- Gradient backgrounds
- Card-based layouts
- Smooth transitions
- Responsive design
- Professional color scheme (blues, greens, grays)

## Notes

- All API calls are handled through the `apiClient` in `lib/api.ts`
- Session management is handled by the backend
- Analysis can take 1-2 minutes depending on document size
- Progress is shown with a dynamic progress bar
