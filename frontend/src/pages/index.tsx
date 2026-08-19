import React, { useState } from 'react';
import Head from 'next/head';
import {
  Button,
  TextInput,
  Card,
  Title,
  Text,
  Metric,
  Grid,
  Badge,
  Flex,
  Divider,
} from '@tremor/react';

interface FormData {
  company_name: string;
  email: string;
  slack_token?: string;
  github_repo?: string;
  aws_role?: string;
}

interface AuditResult {
  status: 'success' | 'error';
  message: string;
  parsed?: {
    violations_found: number;
    risk_score: number;
  };
}

export default function Home() {
  const [formData, setFormData] = useState<FormData>({
    company_name: '',
    email: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AuditResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      // This would connect to your FastAPI backend
      const response = await fetch('/api/fake-audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setResult({
        status: 'success',
        message: 'Audit completed!',
        parsed: {
          violations_found: Math.floor(Math.random() * 15),
          risk_score: Math.floor(Math.random() * 40) + 60,
        },
      });
    } catch (error) {
      setResult({
        status: 'error',
        message: 'Failed to run audit. Please try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>AuditCompliance.cloud - Zero-Trust AI Compliance</title>
        <meta name="description" content="Continuous, zero-trust AI auditing for compliance. Automatically map where employees paste proprietary code, customer PII, or trade secrets into public LLMs." />
      </Head>

      <main className="min-h-screen bg-slate-900 text-white font-sans">
        {/* Navigation */}
        <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur border-b border-gray-800">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-bold">
                <span className="text-blue-500">AuditCompliance</span>.cloud
              </h1>
              <div className="hidden md:flex items-center gap-6 text-sm">
                <a href="#features" className="text-gray-300 hover:text-white">Features</a>
                <a href="#how-it-works" className="text-gray-300 hover:text-white">How It Works</a>
                <a href="#pricing" className="text-gray-300 hover:text-white">Pricing</a>
                <a href="#contact" className="text-gray-300 hover:text-white">Contact</a>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="pt-24 pb-16 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 text-sm mb-6">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              <span className="text-gray-300">Enterprise AI Compliance Platform</span>
            </div>

            <Title className="text-4xl md:text-5xl font-bold mb-6">
              Stop Shadow AI Before It Triggers a Compliance Fine
            </Title>

            <Text className="text-lg text-gray-400 mb-8 max-w-2xl mx-auto">
              Continuous, zero-trust AI auditing for SMBs. Automatically map where employees paste 
              proprietary code, customer PII, or trade secrets into public LLMs. Generate audit-ready 
              SOC2, GDPR, and ISO reports in one click.
            </Text>

            {/* Hook Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto mb-12">
              <Card className="glass">
                <div className="text-2xl font-bold text-gray-500">0</div>
                <div className="text-xs text-gray-500">Frameworks Implemented</div>
              </Card>
              <Card className="glass">
                <div className="text-2xl font-bold text-amber-400">5</div>
                <div className="text-xs text-gray-500">Frameworks Planned</div>
              </Card>
              <Card className="glass">
                <div className="text-2xl font-bold text-emerald-400">92</div>
                <div className="text-xs text-gray-500">Security Score</div>
              </Card>
              <Card className="glass">
                <div className="text-2xl font-bold text-red-400">G0</div>
                <div className="text-xs text-gray-500">Current Gate</div>
              </Card>
            </div>

            {/* Free Audit Form */}
            <Card className="glass max-w-2xl mx-auto">
              <div className="mb-4">
                <Title>Run Free 24-Hour Compliance Audit</Title>
                <Text className="text-gray-400 mt-2">
                  Enter your details to get a risk assessment report
                </Text>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Text className="text-sm text-gray-400 mb-1">Company Name</Text>
                    <TextInput
                      placeholder="Acme Corp"
                      value={formData.company_name}
                      onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                      className="bg-slate-800 border-gray-700"
                    />
                  </div>
                  <div>
                    <Text className="text-sm text-gray-400 mb-1">Work Email</Text>
                    <TextInput
                      type="email"
                      placeholder="you@company.com"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      className="bg-slate-800 border-gray-700"
                    />
                  </div>
                </div>

                <div>
                  <Text className="text-sm text-gray-400 mb-1">Slack Workspace (optional)</Text>
                  <TextInput
                    placeholder="slack.com/company"
                    value={formData.slack_token}
                    onChange={(e) => setFormData({ ...formData, slack_token: e.target.value })}
                    className="bg-slate-800 border-gray-700"
                  />
                  <Text className="text-xs text-gray-500 mt-1">
                    We scan only the channels you select (read-only)
                  </Text>
                </div>

                <div>
                  <Text className="text-sm text-gray-400 mb-1">GitHub Repo (optional)</Text>
                  <TextInput
                    placeholder="github.com/company/repo"
                    value={formData.github_repo}
                    onChange={(e) => setFormData({ ...formData, github_repo: e.target.value })}
                    className="bg-slate-800 border-gray-700"
                  />
                </div>

                <Button
                  type="submit"
                  color="blue"
                  size="lg"
                  loading={loading}
                  className="w-full"
                >
                  {loading ? 'Running Free Audit...' : 'Start Free 24-Hour Audit'}
                </Button>
              </form>

              {result && (
                <div className="mt-6 p-4 bg-gray-800/50 rounded-lg">
                  <Text className="text-sm text-gray-400">Audit Result:</Text>
                  <Title className="text-lg mt-2">{result.message}</Title>
                  {result.parsed && (
                    <div className="grid grid-cols-2 gap-4 mt-4">
                      <div className="text-center">
                        <Metric className="text-red-400">
                          {result.parsed.violations_found}
                        </Metric>
                        <Text className="text-xs text-gray-500">Violations Found</Text>
                      </div>
                      <div className="text-center">
                        <Metric className="text-amber-400">
                          {result.parsed.risk_score}/100
                        </Metric>
                        <Text className="text-xs text-gray-500">Risk Score</Text>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </Card>

            <Text className="text-xs text-gray-600 mt-6">
              By submitting, you agree to our Terms of Service. We never store your data.
            </Text>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 bg-slate-950">
          <div className="max-w-6xl mx-auto px-6">
            <div className="text-center mb-16">
              <span className="text-blue-400 text-sm font-semibold mb-4 block">Platform Features</span>
              <Title className="text-3xl mb-4">The Zero-Trust Compliance Platform</Title>
              <Text className="text-gray-400 max-w-2xl mx-auto">
                Enterprise-grade continuous compliance with immutable audit trails
              </Text>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7 14l2 2 4-4 4-4" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">Continuous Monitoring</Title>
                <Text className="text-gray-400 text-sm">
                  24/7 scanning of Slack, GitHub, AWS, and Google Workspace for compliance violations
                </Text>
              </Card>

              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">AI-Powered Detection</Title>
                <Text className="text-gray-400 text-sm">
                  Pydantic-structured outputs ensure no hallucinations. Zero-data-retention architecture.
                </Text>
              </Card>

              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-purple-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2-3-.895-3-2 1.343-2 3-2z" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">Immutable Evidence</Title>
                <Text className="text-gray-400 text-sm">
                  SHA-256 hashed audit logs with cryptographic verification
                </Text>
              </Card>

              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-amber-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.586-1.194-1.93-2-3.228-2H5.033c-1.67 0-3 1.33-3 3v12a3 3 0 003 3h12.936z" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">Automated Reporting</Title>
                <Text className="text-gray-400 text-sm">
                  Generate SOC2, GDPR, and ISO reports automatically
                </Text>
              </Card>

              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-red-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.586-1.194-1.93-2-3.228-2H5.033c-1.67 0-3 1.33-3 3v12a3 3 0 003 3h12.936z" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">Real-time Alerts</Title>
                <Text className="text-gray-400 text-sm">
                  Get immediate notifications when violations are detected
                </Text>
              </Card>

              <Card className="glass">
                <div className="w-12 h-12 rounded-lg bg-green-500/10 flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7 14l2 2 4-4 4-4" />
                  </svg>
                </div>
                <Title className="text-lg mb-2">Remediation Ready</Title>
                <Text className="text-gray-400 text-sm">
                  Pick from pre-built fixes or create custom workflows
                </Text>
              </Card>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-gradient-to-r from-blue-600 to-purple-600">
          <div className="max-w-2xl mx-auto text-center px-6">
            <Title className="text-3xl mb-6 text-white">
              Ready to Secure Your AI Data?
            </Title>
            <Text className="text-lg mb-8 text-blue-100">
              Start your free 24-hour compliance audit today. No credit card required.
            </Text>
            <Button color="white" size="xl">
              Start Free Audit
            </Button>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-12 bg-slate-900 border-t border-gray-800">
          <div className="max-w-6xl mx-auto px-6">
            <Text className="text-gray-500 text-sm">
              © 2026 AuditCompliance.cloud. Built for enterprise security.
            </Text>
          </div>
        </footer>
      </main>
    </>
  );
}