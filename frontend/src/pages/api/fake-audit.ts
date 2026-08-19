/**
 * Fake Audit Endpoint for Landing Page Demonstration
 * This simulates the backend API response for the free audit form
 */

import type { NextApiRequest, NextApiResponse } from 'next';
import { v4 as uuidv4 } from 'uuid';

type ComplianceFramework = 'SOC2' | 'GDPR' | 'HIPAA' | 'ISO27001' | 'NONE';

interface AuditResponse {
  status: 'success' | 'error';
  message: string;
  data?: {
    run_id: string;
    compliance_score: number;
    violations_found: number;
    critical_violations: number;
    framework_status: Array<{
      framework: ComplianceFramework;
      status: 'ready' | 'warning' | 'critical';
      score: number;
    }>;
    evidence_available: boolean;
    report_url?: string;
  };
}

// Simulate finding violations based on input
function simulateAudit(data: {
  company_name: string;
  email: string;
  slack_token?: string;
  github_repo?: string;
  aws_role?: string;
}): AuditResponse {
  const runId = uuidv4();
  
  // Simulate realistic findings based on input
  let violations = 0;
  let critical = 0;

  // Companies with more integrations tend to have more violations
  if (data.slack_token) violations += 3;
  if (data.github_repo) violations += 5;
  if (data.aws_role) violations += 2;

  // Add base violations
  violations += Math.floor(Math.random() * 10);
  critical = Math.floor(violations * 0.3);

  const score = Math.max(0, 100 - violations * 2 - critical * 5);

  return {
    status: 'success',
    message: 'Free 24-hour audit completed successfully',
    data: {
      run_id: runId,
      compliance_score: score,
      violations_found: violations,
      critical_violations: critical,
      framework_status: [
        { framework: 'SOC2', status: score > 80 ? 'ready' : score > 60 ? 'warning' : 'critical', score },
        { framework: 'GDPR', status: 'warning', score: score - 5 },
        { framework: 'HIPAA', status: 'ready', score: score + 5 },
        { framework: 'ISO27001', status: 'ready', score: score + 2 },
      ],
      evidence_available: true,
      report_url: `/reports/${runId}.pdf`,
    },
  };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AuditResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ status: 'error', message: 'Method not allowed' });
  }

  try {
    const { company_name, email, slack_token, github_repo, aws_role } = req.body;

    if (!company_name || !email) {
      return res.status(400).json({
        status: 'error',
        message: 'Company name and email are required',
      });
    }

    // Simulate API delay for realism
    await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));

    const result = simulateAudit({
      company_name,
      email,
      slack_token,
      github_repo,
      aws_role,
    });

    // Add cache control headers
    res.setHeader('Cache-Control', 'no-store, max-age=0');
    res.setHeader('X-Generated-By', 'AuditCompliance.ai');

    return res.status(200).json(result);
  } catch (error) {
    console.error('Audit error:', error);
    return res.status(500).json({
      status: 'error',
      message: 'Audit failed. Please try again.',
    });
  }
}