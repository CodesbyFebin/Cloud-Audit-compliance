import React, { useState } from 'react';
import { Card, Title, Text, Badge, Divider, Button, Metric } from "@tremor/react";
import { AlertCircle, ShieldCheck, Trash2, Copy } from "lucide-react";

interface Violation {
  id: string;
  violation_type: 'PII_LEAK' | 'CREDENTIAL_LEAK' | 'SHADOW_AI' | 'PROPRIETARY_IP' | 'SENSITIVE_DATA';
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  evidence_snippet: string;
  implicated_framework_clauses: string[];
  recommended_action: string;
  confidence_score?: number;
  timestamp: string;
  is_resolved?: boolean;
}

interface ViolationCardProps {
  violation: Violation;
  onResolve: (id: string) => void;
  onDelete: (id: string) => void;
}

const severityColorMap: Record<string, string> = {
  CRITICAL: "red",
  HIGH: "orange", 
  MEDIUM: "yellow",
  LOW: "blue",
};

const violationTypeLabels: Record<string, string> = {
  PII_LEAK: "PII Leak",
  CREDENTIAL_LEAK: "Credential Leak",
  SHADOW_AI: "Shadow AI",
  PROPRIETARY_IP: "Proprietary IP",
  SENSITIVE_DATA: "Sensitive Data"
};

export default function ViolationCard({ violation, onResolve, onDelete }: ViolationCardProps) {
  const [copied, setCopied] = useState(false);
  
  const handleCopy = async () => {
    await navigator.clipboard.writeText(violation.evidence_snippet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card className="hover:shadow-lg transition-all duration-200 border border-gray-800/50">
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center gap-2">
          <Badge color={severityColorMap[violation.severity]} size="sm">
            {violation.severity}
          </Badge>
          <Title className="text-sm font-medium">
            {violationTypeLabels[violation.violation_type]}
          </Title>
        </div>
        <div className="text-xs text-gray-500">
          {new Date(violation.timestamp).toLocaleString()}
        </div>
      </div>

      <Divider className="my-2" />

      <Text className="text-sm mb-3 line-clamp-3 text-gray-300">
        {violation.evidence_snippet}
      </Text>

      {violation.confidence_score && (
        <div className="flex items-center gap-2 mb-3">
          <div className="text-xs text-gray-500">Confidence:</div>
          <Metric className="text-xs font-mono">
            {(violation.confidence_score * 100).toFixed(1)}%
          </Metric>
        </div>
      )}

      {violation.implicated_framework_clauses.length > 0 && (
        <div className="mb-3">
          <Text className="text-xs text-gray-400 mb-1">Affected Frameworks:</Text>
          <div className="flex flex-wrap gap-1">
            {violation.implicated_framework_clauses.map((clause, index) => (
              <Badge key={index} color="gray" size="sm">
                {clause}
              </Badge>
            ))}
          </div>
        </div>
      )}

      <div className="bg-gray-900/30 rounded-lg p-3 mb-3">
        <Text className="text-xs text-gray-400">Recommended Action:</Text>
        <Text className="text-sm text-gray-200 mt-1">
          {violation.recommended_action}
        </Text>
      </div>

      <div className="flex gap-2">
        <Button
          size="sm"
          color="emerald"
          icon={ShieldCheck}
          onClick={() => onResolve(violation.id)}
          disabled={violation.is_resolved}
        >
          {violation.is_resolved ? "Resolved" : "Mark Resolved"}
        </Button>
        
        <Button
          size="sm"
          color="gray"
          icon={Copy}
          onClick={handleCopy}
          variant="secondary"
        >
          {copied ? "Copied!" : "Copy"}
        </Button>

        <Button
          size="sm"
          color="red"
          icon={Trash2}
          onClick={() => onDelete(violation.id)}
          variant="ghost"
        >
          Delete
        </Button>
      </div>
    </Card>
  );
}