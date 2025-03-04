#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>
#include <cmath>
#include <bitset>
#include <numeric>
#include <chrono>
#define MAX_SIZE_OF_SUBSET 19
#define MAX_COST_OF_WAY 100000

struct PathInfo;

using AdjacencyMatrix = std::vector<std::vector<int>>;

/*
* Данная структура хранит номер узла (endNodeName),
* на котором заканчивается данное подмножетсво узлов
* и стоимость пути, проходящего через данное подмножество узлов
* и заканчивающегося в endNodeName.
*/
struct PathInfo {
    int endNodeName;
    int costOfPath;
    std::vector<int> path;
};


class Graph {
public:
    /*
    * Данный метод предназначен для считывания графа из файла.
    * В файле на самом деле хранится матрица смежности,
    * которая в ходе алгоритма переписывается в матрицу
    * смежности, но которая теперь хранится в программе в виде
    * структуры данных
    */
    void ReadGraph() {
        std::string edgeWeight, lineOfInputFile;
        std::vector<int> edgesWeights;
        std::stringstream lineOfInputFileStream;
        std::ifstream inputFile("graph2.txt");
        if (inputFile.is_open())
        {
            while (getline(inputFile, lineOfInputFile))
            {
                lineOfInputFileStream.str(lineOfInputFile);
                while (getline(lineOfInputFileStream, edgeWeight, ' ')) {
                    edgesWeights.push_back(std::stoi(edgeWeight));
                }
                graphStorage_.push_back(edgesWeights);
                edgesWeights.clear();
                lineOfInputFileStream.clear();
            }
        }
        inputFile.close();
    }
    /*
    * Данный метод предназначен для получения
    * считанной из файла матрицы смежности.
    * Выходные данные: матрица смежности графа.
    */
    AdjacencyMatrix GetGraphStorage() {
        return graphStorage_;
    }
private:
    AdjacencyMatrix graphStorage_;
};


class TravellingSalesmanProblem {
public:
    /*
    * Конструктор для инициализации матрицы смежности
    * в данном классе считанной матрицей смежности
    * в методе ReadGraph класса Graph.
    */
    TravellingSalesmanProblem(AdjacencyMatrix graphStorage) {
        this->graphStorage_ = graphStorage;
        this->numbOfExistingPathsInSubsets_ = 0;
        this->minCostOfWayInSubset_ = MAX_COST_OF_WAY;
        this->pathWasntFound_ = false;
    }
    /*
    * Данный метод запускает решение TSP с помощью
    * алгоритма Беллмана-Хелда-Карпа и фиксрует время 
    * начала и конца работы алгоритма
    * Запускаются следующие методы: генерация подмножеств,
    * поиск минимального по стоимости гамильтонова цикла,
    * печать ответа на экран
    */
    void Run() {
        startTime_ = std::chrono::steady_clock::now();
        GenerateSubsetsOfNodes();
        FindCheapestHamiltonianCycle();
        PrintAnswer();
    }
    

private:
    /*
    * Данный метод генерирует всевозможные подмножества множества
    * узлов {2, 3, .., n} с помощью битовых масок длины n - 1,
    * где если i-ый элемент подмножесва (начиная с 0)
    * равен 1, значит (i + 2)-ый узел входит в данное подмножество,
    * иначе -- не входит.
    * Например: дана маска 1011
    * |i   |0|1|2|3|
    * |mask|1|0|1|1|
    * Следов-но, в подмножество, которое представляетcя в виде вектора,
    * войдёт следующий набор узлов: {2, 4, 5}
    */
    void GenerateSubsetsOfNodes() {
        int subsetPrototype = 1;
        int maxPowerOfSubset = (int)(graphStorage_.size() - 1);
        while (subsetPrototype < (int)pow(2, maxPowerOfSubset)) {
            std::bitset<MAX_SIZE_OF_SUBSET> dirtySubsetBitForm(subsetPrototype);
            costTable_[GetCleanSubset(dirtySubsetBitForm.to_string())] = {};
            subsetPrototype++;
        }
    }
    /*
    * Данный метод представляет собой запуск алгоритма Беллмана-Хелда-Карпа.
    * На уровне этого метода происходит инициализация информации о единичных 
    * подмножествах и перебор всех подмножеств узлов каждого размера(мощности).
    */
    void FindCheapestHamiltonianCycle() {
        for (int i = 2; i <= graphStorage_.size(); i++) {
            costTable_[{i}].push_back({ i, graphStorage_[0][i - 1], {1, i} });
        }
        for (int powerOfSubset = 2; powerOfSubset < graphStorage_.size(); powerOfSubset++) {
            numbOfExistingPathsInSubsets_ = 0;
            for (auto subsetInfo : costTable_) {
                if (subsetInfo.first.size() == powerOfSubset) {
                    IteratingThroughSubsetWithoutNode(subsetInfo.first);
                }
            }
            if (!numbOfExistingPathsInSubsets_) {
                pathWasntFound_ = true;
                return;
            }
        }
        numbOfExistingPathsInSubsets_ = 0;
        std::vector<int> subset(graphStorage_.size() - 1);
        std::iota(subset.begin(), subset.end(), 2);
        FindMinCostOfPathInSubset(subset, 1);
        if (!numbOfExistingPathsInSubsets_) {
            pathWasntFound_ = true;
        }
        else {
            minCostOfHamiltonianCycle_ = minCostOfWayInSubset_;
            nodesOfMinCostedHamiltonianCycle_ = nodesOfMinCostedWayInSubset_;
            nodesOfMinCostedHamiltonianCycle_.push_back(1);
        }
    }
    /*
    * Данный метод предназначен для перебора всех подмножеств
    * S\{k}, где k -- узел, принадлежащий множеству S.
    * Входные данные: подмножество в виде вектора
    */
    void IteratingThroughSubsetWithoutNode(std::vector<int> subset) {
        PathInfo pathInfo{ 0, 0, {} };
        std::vector<int> subsetWithoutOneNode;
        for (int i = 0; i < subset.size(); i++) {
            subsetWithoutOneNode = subset;
            subsetWithoutOneNode.erase(subsetWithoutOneNode.begin() + i);
            FindMinCostOfPathInSubset(subsetWithoutOneNode, subset[i]);
            nodesOfMinCostedWayInSubset_.push_back(subset[i]);
            pathInfo.endNodeName = subset[i];
            pathInfo.costOfPath = minCostOfWayInSubset_;
            pathInfo.path = nodesOfMinCostedWayInSubset_;
            costTable_[subset].push_back(pathInfo);
        }
    }
    /*
    * Данный метод предназначен для поиска минимального по стоимости пути
    * в данном подмножестве
    * Входные данные: подмножество в виде вектора и узел,
    * в котором заканчивается путь множества.
    */
    void FindMinCostOfPathInSubset(std::vector<int>&subset, int nodeName) {
        nodesOfMinCostedWayInSubset_.clear();
        minCostOfWayInSubset_ = MAX_COST_OF_WAY;
        for (auto const& pathInfo : costTable_[subset]) {
            if (pathInfo.costOfPath + graphStorage_[pathInfo.endNodeName - 1][nodeName - 1] < minCostOfWayInSubset_) {
                minCostOfWayInSubset_ = pathInfo.costOfPath +
                    graphStorage_[pathInfo.endNodeName - 1][nodeName - 1];
                nodesOfMinCostedWayInSubset_ = pathInfo.path;
            }
        }
        if (minCostOfWayInSubset_ != MAX_COST_OF_WAY) {
            numbOfExistingPathsInSubsets_++;
        }
    }
    /*
    * Данный метод предназначен для очистки битового
    * представления подмножеств от лишних нулей,
    * которые появились в силу перевода в двоичную
    * систему счисления с помощью std::bitset и интерпретации
    * таких подмножеств в виде вектора.
    */
    std::vector<int> GetCleanSubset(std::string subsetInBitForm) {
        std::string cleanSubsetInBitForm = subsetInBitForm.substr(subsetInBitForm.size() - graphStorage_.size() + 1, 
            graphStorage_.size() - 1);
        std::vector<int> cleanSubset;
        for (int i = 0; i < cleanSubsetInBitForm.size(); i++) {
            if (cleanSubsetInBitForm[i] == '1') {
                cleanSubset.push_back(i + 2);
            }
        }
        return cleanSubset;
    }
    /*
    * Данный метод предназначен для печати ответа на экран
    */
    void PrintAnswer() {
        auto endTime = std::chrono::steady_clock::now();
        auto spentTime = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime_);
        if (pathWasntFound_) {
            std::cout << "Path doesn't exists." << " " << spentTime.count() << "ms" << std::endl;
        }
        else { 
            std::cout << "[";
            int lenOfCycle = (int)nodesOfMinCostedHamiltonianCycle_.size();
            for (int i = 0; i < lenOfCycle - 1; i++) {
                std::cout << nodesOfMinCostedHamiltonianCycle_[i] << ", ";
            }
            std::cout << nodesOfMinCostedHamiltonianCycle_[lenOfCycle - 1] << "], ";
            std::cout << minCostOfHamiltonianCycle_ << ", ";
            std::cout << spentTime.count() << " ms" << std::endl;
        }
    }

    AdjacencyMatrix graphStorage_;
    std::map<std::vector<int>, std::vector<PathInfo>> costTable_;
    int numbOfExistingPathsInSubsets_;
    std::vector<int> nodesOfMinCostedHamiltonianCycle_, nodesOfMinCostedWayInSubset_;
    int minCostOfHamiltonianCycle_, minCostOfWayInSubset_;
    bool pathWasntFound_;
    std::chrono::steady_clock::time_point startTime_;
};
int main() {
    Graph graph;
    graph.ReadGraph();
    TravellingSalesmanProblem tsp(graph.GetGraphStorage());
    tsp.Run();
    return 0;
}
