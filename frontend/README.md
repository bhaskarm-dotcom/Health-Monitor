# Frontend - AI Project Health Monitor

Next.js frontend dashboard for the AI-Powered Project Health Monitor system.

## Structure

- `app/` - Next.js app directory
  - `page.tsx` - Main dashboard page
  - `layout.tsx` - Root layout
  - `globals.css` - Global styles
- `components/` - React components
  - `HealthScore.tsx` - Health score display
  - `DimensionBreakdown.tsx` - Dimension breakdown visualization
  - `RiskSummary.tsx` - Risk summary display
  - `Recommendations.tsx` - AI recommendations display
  - `TrendChart.tsx` - Health score trend chart
- `lib/api.ts` - API client and types

## Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Building for Production

```bash
npm run build
npm start
```

