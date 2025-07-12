@echo off

echo Building the project...
call mvn clean package

if %ERRORLEVEL% EQU 0 (
    echo Build successful!
    echo Running phylogenetic analysis...
    
    if "%~1"=="" (
        java -jar target\phylogenetic-analysis-1.0.0.jar
    ) else (
        java -jar target\phylogenetic-analysis-1.0.0.jar %1
    )
) else (
    echo Build failed!
    exit /b 1
)