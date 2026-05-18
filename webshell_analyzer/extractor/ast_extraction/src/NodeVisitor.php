<?php

namespace NodeVisitor;

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/featuresDeclare.php';

use Features\featureWrapper;
use PhpParser\NodeVisitorAbstract;
use PhpParser\Node;
use PhpParser\Node\Name;
use PhpParser\Node\Expr;
use PhpParser\Node\Stmt;

class NodeVisitor extends NodeVisitorAbstract {
    private featureWrapper $features;
    private array $superglobal = ['_GET', '_POST', '_COOKIE', '_REQUEST', '_FILES', '_ENV', '_SERVER', '_SESSION', 'GLOBALS'];

     public function __construct(featureWrapper $features){
        $this->features = $features;
    }

    public function enterNode(Node $node) {
        $this->handleDynamicFeatures($node);
        $this->handleStructuralFeatures($node);
    }
    
    private function getFuncName(Node $node): ?string {
        if($node instanceof Expr\FuncCall && $node->name instanceof Name){
            return strtolower($node->name->toString());
        }
        return null;
    }

    private function isSuperglobal(Node $node): bool {
        return $node instanceof Expr\ArrayDimFetch && $node->var instanceof Expr\Variable && is_string($node->var->name) && in_array($node->var->name, $this->superglobal);
    }

    private function handleDynamicFeatures(Node $node){
        #dynamic function call exists (dynamicFuncCallExists feature)
        if($node instanceof Expr\FuncCall && $node->name instanceof Expr\Variable){
            $this->features->dynamicFeatures->dynamicFuncCallExists = true;
        }
        #check for variable variables (varExists feature)
        if($node instanceof Expr\Variable && $node->name instanceof Expr\Variable){
            $this->features->dynamicFeatures->varExists = true;
        }
        #count variable usage (varUsageCount feature)
        if($node instanceof Expr\Variable){
            $this->features->dynamicFeatures->varUsageCount++;
        }
        #count assignments (assignmentCount feature)
        if($node instanceof Expr\Assign){
            $this->features->dynamicFeatures->assignmentCount++;
        }
    }

    private function handleStructuralFeatures(Node $node) {

        #class definition exists (classDefExists feature)
        if($node instanceof Stmt\Class_){
            $this->features->structuralFeatures->classDefExists = true;
        }

        #count function definitions (funcDefCount feature)
        if($node instanceof Stmt\Function_ || $node instanceof Stmt\ClassMethod){
            $this->features->structuralFeatures->funcDefCount++;
        }

        #count superglobal used as function argument (superglobalAsFuncArg feature)
        if($node instanceof Expr\FuncCall ){
            foreach($node->args as $arg){
                if($this->isSuperglobal($arg->value)){
                    $this->features->structuralFeatures->superglobalAsFuncArg++;
                }
            }
        }

        #count suspicious concatenation (suspiciousConcat feature)
        if($node instanceof Expr\BinaryOp\Concat){
            $this->features->structuralFeatures->suspiciousConcat = ($this->features->structuralFeatures->suspiciousConcat ?? 0) + 1;
        }
    }
}
?>