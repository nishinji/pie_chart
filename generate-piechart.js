const axios = require("axios");
const fs = require("fs");

// Vita3K APIからデータを取得してSVGを生成
async function generateSVG() {
    try {
        const response = await axios.get("https://vita3k-api.pedro.moe/list/commercial");
        const data = response.data;

        const counts = {
            Nothing: 0,
            Bootable: 0,
            Intro: 0,
            Menu: 0,
            "Ingame -": 0,
            "Ingame +": 0,
            Playable: 0,
        };

        data.forEach(game => {
            if (counts.hasOwnProperty(game.status)) {
                counts[game.status]++;
            }
        });

        const total = Object.values(counts).reduce((sum, count) => sum + count, 0);

        let cumulativePercentage = 0;
        const colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#4CAF50"];
        let svgPaths = "";

        Object.entries(counts).forEach(([status, count], index) => {
            const percentage = count / total;
            const startAngle = cumulativePercentage * 2 * Math.PI;
            const endAngle = (cumulativePercentage + percentage) * 2 * Math.PI;

            const x1 = 16 + 16 * Math.cos(startAngle);
            const y1 = 16 + 16 * Math.sin(startAngle);
            const x2 = 16 + 16 * Math.cos(endAngle);
            const y2 = 16 + 16 * Math.sin(endAngle);

            const largeArcFlag = percentage > 0.5 ? 1 : 0;

            svgPaths += `
<path d="M16 16 L${x1} ${y1} A16 16 0 ${largeArcFlag} 1 ${x2} ${y2} Z"
      fill="${colors[index % colors.length]}">
</path>`;
            cumulativePercentage += percentage;
        });

        const svg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="400" height="400">
    ${svgPaths}
    <circle cx="16" cy="16" r="10" fill="white"></circle>
    <text x="16" y="16" text-anchor="middle" font-size="2" fill="black" dy=".3em">Vita3K</text>
</svg>
        `;

        // SVGをファイルに保存
        fs.writeFileSync("output.svg", svg);
        console.log("SVG file has been generated: output.svg");
    } catch (error) {
        console.error("Error fetching data from Vita3K API:", error);
    }
}

// 実行
generateSVG();
