# Check Agent Error Details
Write-Host "Checking agent error details..." -ForegroundColor Cyan
Write-Host ""

# Get full agent details
$agent = aws bedrock-agent get-agent --agent-id KKKWOGHCCZ | ConvertFrom-Json

Write-Host "Agent Status: $($agent.agent.agentStatus)" -ForegroundColor Yellow
Write-Host ""

if ($agent.agent.failureReasons) {
    Write-Host "Failure Reasons:" -ForegroundColor Red
    $agent.agent.failureReasons | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor Red
    }
} else {
    Write-Host "No failure reasons provided" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Full Agent Details:" -ForegroundColor Cyan
$agent.agent | ConvertTo-Json -Depth 10
