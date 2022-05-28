module.exports = {
    branches: ["master", "beta"],
    repositoryUrl: "https://github.com/Phenomenon2919/SimpleMonetaryTracker",
    plugins: [
        '@semantic-release/commit-analyzer',
        '@semantic-release/release-notes-generator',
        ['@semantic-release/github',{
            "assets": [
                {"path":"dist/SimpleMonetaryTracker.exe","name":"SimpleMonetaryTracker","label":"Simple Monetary Tracker Executable"}
            ]
        }]
    ]
}